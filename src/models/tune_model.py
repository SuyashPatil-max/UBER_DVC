import argparse
import logging
import json
import os
from pathlib import Path

import dagshub
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import numpy as np
import optuna
import pandas as pd
import seaborn as sns
import yaml
from catboost import CatBoostClassifier
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from mlflow.models.signature import infer_signature
from sklearn.metrics import (
    confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score,
    average_precision_score, balanced_accuracy_score, matthews_corrcoef, precision_recall_curve
)
from sklearn.model_selection import train_test_split

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s- %(levelname)s - %(message)s",
)

optuna.logging.set_verbosity(optuna.logging.WARNING)

logging.info("Setting mlflow and dagshub : ")

token = os.getenv("DAGSHUB_TOKEN")
if token:
    dagshub.auth.add_app_token(token)

mlflow.set_tracking_uri("https://dagshub.com/SuyashPatil-max/UBER_DVC.mlflow")
dagshub.init(
    repo_owner='SuyashPatil-max',
    repo_name='UBER_DVC',
    mlflow=True
)
logging.info("Setting mlflow and dagshub finised ")


def load_paths():
    try:
        paths = Path(__file__).resolve().parents[2]
        data_path = paths / "data" / "processed"
        reports_path = paths / "reports"

        return {
            "reports": reports_path,
            "tuning_cm_path": reports_path / "tuning_cm.png",
            "tuning_pr_curve_path": reports_path / "tuning_pr_curve.png",
            "tuning_metrics_path": reports_path / "tuning_metrics.json",
            "tuning_trials_path": reports_path / "tuning_trials.csv",
            "tuning_study_db": reports_path / "tuning_study.db",
            "params_path": paths / "params.yaml",
            "X_train_path": data_path / "X_train.csv",
            "X_test_path": data_path / "X_test.csv",
            "y_train_path": data_path / "y_train.csv",
            "y_test_path": data_path / "y_test.csv",
        }
    except Exception as e:
        logging.error(f"Error in loading paths : {e}")
        raise e


def load_params(params_path):
    try:
        with open(params_path, "r") as f:
            params = yaml.safe_load(f)
        return params
    except Exception as e:
        logging.error(f"params not loaded : {e}")
        raise e


def load_data(data_path) -> pd.DataFrame:
    try:
        logging.info(f"Loading {data_path} dataset")
        return pd.read_csv(data_path)
    except Exception as e:
        logging.error(f"Error in loading {data_path} dataset : {e}")
        raise e


def build_pipeline(cat_params, smote_params):
    return Pipeline(
        [
            ("smote", SMOTE(**smote_params)),
            ("catboost", CatBoostClassifier(**cat_params)),
        ]
    )


def make_objective(X_tr, y_tr, X_val, y_val, base_cat_params, base_smote_params, random_seed):
    def objective(trial):
        try:
            positive_weight = trial.suggest_float("class_weight_positive", 1.0, 10.0)
            cat_params = {
                **base_cat_params,
                "iterations": 3000,
                "learning_rate": trial.suggest_float("learning_rate", 1e-3, 0.3, log=True),
                "depth": trial.suggest_int("depth", 3, 10),
                "l2_leaf_reg": trial.suggest_float("l2_leaf_reg", 1.0, 15.0, log=True),
                "bagging_temperature": trial.suggest_float("bagging_temperature", 0.0, 10.0),
                "border_count": trial.suggest_int("border_count", 32, 255),
                "class_weights": [1, positive_weight],
                "verbose": False,
                "random_seed": random_seed,
            }
            smote_params = {
                **base_smote_params,
                "sampling_strategy": trial.suggest_float("sampling_strategy", 0.4, 1.0),
                "k_neighbors": trial.suggest_int("k_neighbors", 3, 10),
                "random_state": random_seed,
            }

            model = build_pipeline(cat_params, smote_params)
            model.fit(
                X_tr,
                y_tr,
                catboost__eval_set=(X_val, y_val),
                catboost__early_stopping_rounds=50,
                catboost__use_best_model=True,
            )

            y_pred = model.predict(X_val)
            y_val_probs = model.predict_proba(X_val)[:, -1]
            recall = recall_score(y_val, y_pred)
            f1 = f1_score(y_val, y_pred)

            # Optimization stays on (recall, f1) so the resumable optuna study
            # keeps the same two-objective shape it was created with. These
            # extra ones are logged purely for visibility per trial - with a
            # ~10:1 imbalance, pr_auc/balanced_accuracy/mcc are the metrics
            # worth eyeballing across trials, roc_auc alone would be misleading.
            pr_auc = average_precision_score(y_val, y_val_probs)
            balanced_acc = balanced_accuracy_score(y_val, y_pred)
            mcc = matthews_corrcoef(y_val, y_pred)

            best_iteration = model.named_steps["catboost"].get_best_iteration()
            trial.set_user_attr("best_iteration", int(best_iteration) if best_iteration is not None else cat_params["iterations"])

            try:
                with mlflow.start_run(run_name=f"trial_{trial.number}", nested=True):
                    mlflow.log_params({f"catboost_{k}": v for k, v in cat_params.items()})
                    mlflow.log_params({f"smote_{k}": v for k, v in smote_params.items()})
                    mlflow.log_metrics({
                        "recall": recall,
                        "f1_score": f1,
                        "pr_auc": pr_auc,
                        "balanced_accuracy": balanced_acc,
                        "mcc": mcc,
                    })
            except Exception as mlflow_err:
                logging.warning(f"Trial {trial.number} mlflow logging failed : {mlflow_err}")

            return recall, f1

        except Exception as e:
            logging.warning(f"Trial {trial.number} failed due to : {e}")
            return 0.0, 0.0

    return objective


def log_trial(study, trial):
    recall, f1 = trial.values
    logging.info(f"Trial {trial.number} finished - recall: {recall:.4f}, f1: {f1:.4f}")


def select_best_trial(study):
    pareto_trials = [t for t in study.best_trials if t.values is not None]
    if not pareto_trials:
        raise RuntimeError("No successful trials to select from")
    return max(pareto_trials, key=lambda t: sum(t.values))


def tune(params, X_train, y_train, n_trials, timeout, study_db_path):
    random_seed = params["cat_model"].get("random_seed", 42)

    X_tr, X_val, y_tr, y_val = train_test_split(
        X_train,
        y_train,
        test_size=params["build_feature"]["test_size"],
        random_state=params["build_feature"]["random_state"],
        stratify=y_train,
    )

    base_cat_params = {
        k: v for k, v in params["cat_model"].items() if k not in ("class_weights",)
    }
    base_smote_params = {}

    study = optuna.create_study(
        directions=["maximize", "maximize"],
        sampler=optuna.samplers.TPESampler(seed=random_seed, multivariate=True),
        study_name="uber_catboost_tuning",
        storage=f"sqlite:///{study_db_path}",
        load_if_exists=True,
    )

    objective = make_objective(X_tr, y_tr, X_val, y_val, base_cat_params, base_smote_params, random_seed)
    study.optimize(objective, n_trials=n_trials, timeout=timeout, callbacks=[log_trial])

    best_trial = select_best_trial(study)
    logging.info(f"Best trial {best_trial.number} - recall: {best_trial.values[0]:.4f}, f1: {best_trial.values[1]:.4f}")

    return study, best_trial


def build_tuned_params(params, best_trial):
    tuned_params = json.loads(json.dumps(params))

    tuned_params["cat_model"]["learning_rate"] = best_trial.params["learning_rate"]
    tuned_params["cat_model"]["depth"] = best_trial.params["depth"]
    tuned_params["cat_model"]["l2_leaf_reg"] = best_trial.params["l2_leaf_reg"]
    tuned_params["cat_model"]["bagging_temperature"] = best_trial.params["bagging_temperature"]
    tuned_params["cat_model"]["border_count"] = best_trial.params["border_count"]
    tuned_params["cat_model"]["class_weights"] = [1, best_trial.params["class_weight_positive"]]
    tuned_params["cat_model"]["iterations"] = best_trial.user_attrs["best_iteration"] + 1

    tuned_params["smote"]["sampling_strategy"] = best_trial.params["sampling_strategy"]
    tuned_params["smote"]["k_neighbors"] = best_trial.params["k_neighbors"]

    return tuned_params


def retrain_and_evaluate(tuned_params, X_train, y_train, X_test, y_test):
    logging.info("Retraining final model on full training data with tuned hyperparameters : ")

    cat_params = dict(tuned_params["cat_model"])
    smote_params = dict(tuned_params["smote"])

    model = build_pipeline(cat_params, smote_params)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_probs = model.predict_proba(X_test)[:, -1]
    y_true = np.asarray(y_test).ravel()

    metrics = {
        "recall": recall_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "f1_score": f1_score(y_true, y_pred),
        "roc_auc": roc_auc_score(y_true, y_probs),
        "pr_auc": average_precision_score(y_true, y_probs),
        "balanced_accuracy": balanced_accuracy_score(y_true, y_pred),
        "mcc": matthews_corrcoef(y_true, y_pred),
        "positive_class_prevalence": float(y_true.mean()),
    }
    cm = confusion_matrix(y_true, y_pred)

    return metrics, cm, model, y_probs


def cm_to_heatmap(cm, cm_path):
    try:
        logging.info(f"Saving the cm to {cm_path}")
        plt.figure(figsize=(12, 8))
        sns.heatmap(cm, cmap="Blues", annot=True, fmt="d")
        plt.savefig(cm_path, dpi=300, bbox_inches="tight")
        plt.close()
    except Exception as e:
        logging.error(f"Error occured in saving cm : {e}")
        raise e


def pr_curve_plot(y_test, y_probs, pr_curve_path):
    try:
        logging.info(f"Saving the PR curve to {pr_curve_path}")
        y_true = np.asarray(y_test).ravel()
        precision, recall, _ = precision_recall_curve(y_true, y_probs)
        baseline = y_true.mean()

        plt.figure(figsize=(10, 7))
        plt.plot(recall, precision, label="CatBoost + SMOTE (tuned)")
        plt.axhline(baseline, color="grey", linestyle="--",
                    label=f"Random baseline (prevalence = {baseline:.3f})")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title("Precision-Recall curve (positive class = Incomplete)")
        plt.legend()
        plt.savefig(pr_curve_path, dpi=300, bbox_inches="tight")
        plt.close()
    except Exception as e:
        logging.error(f"Error occured in saving pr curve : {e}")
        raise e


def save_outputs(study, tuned_params, metrics, baseline_metrics, paths):
    study.trials_dataframe().to_csv(paths["tuning_trials_path"], index=False)

    with open(paths["tuning_metrics_path"], "w") as f:
        json.dump(
            {
                "tuned_metrics": metrics,
                "baseline_metrics": baseline_metrics,
                "best_cat_model_params": tuned_params["cat_model"],
                "best_smote_params": tuned_params["smote"],
            },
            f,
            indent=4,
        )

    with open(paths["params_path"], "w") as f:
        yaml.safe_dump(tuned_params, f, sort_keys=False)

    logging.info(f"Tuned params written back to {paths['params_path']}")


def log_final_run(model, metrics, tuned_params, best_trial, train_data, test_data, params_path, cm_path, pr_curve_path, X_train, X_test, reports_path):
    try:
        logging.info("Logging tuned model and artifacts to mlflow : ")

        cat_params = {f"catboost_{k}": v for k, v in tuned_params["cat_model"].items()}
        smote_params = {f"smote_{k}": v for k, v in tuned_params["smote"].items()}

        mlflow.log_metrics(metrics)
        mlflow.log_params(cat_params)
        mlflow.log_params(smote_params)
        mlflow.log_param("optuna_best_trial_number", best_trial.number)

        train_dataset = mlflow.data.from_pandas(train_data)
        test_dataset = mlflow.data.from_pandas(test_data)
        mlflow.log_input(train_dataset, context="train_data")
        mlflow.log_input(test_dataset, context="test_data")

        mlflow.log_artifact(params_path)
        mlflow.log_artifact(cm_path)
        mlflow.log_artifact(pr_curve_path)

        sig = infer_signature(X_train, model.predict(X_test))
        model_info = mlflow.sklearn.log_model(
            model,
            "cat_smote_tuned_model",
            signature=sig,
            serialization_format="pickle",
        )

        with open(reports_path / "tuning_experiment.json", "w") as f:
            json.dump(
                {
                    "run_id": mlflow.active_run().info.run_id,
                    "model_uri": model_info.model_uri,
                },
                f,
            )

        logging.info("Logging of tuned model to mlflow completed")

    except Exception as e:
        logging.error(f"Error logging tuned model to mlflow : {e}")
        raise e


def load_baseline_metrics(reports_path):
    metrics_path = reports_path / "metrics.json"
    if not metrics_path.exists():
        return None
    with open(metrics_path, "r") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Hyperparameter tuning for the CatBoost ride-completion model")
    parser.add_argument("--n_trials", type=int, default=40)
    parser.add_argument("--timeout", type=int, default=None, help="Timeout in seconds for the whole study")
    args = parser.parse_args()

    try:
        paths = load_paths()
        params = load_params(paths["params_path"])

        X_train = load_data(paths["X_train_path"])
        X_test = load_data(paths["X_test_path"])
        y_train = load_data(paths["y_train_path"])
        y_test = load_data(paths["y_test_path"])

        train_data = pd.concat([X_train, y_train], axis=1)
        test_data = pd.concat([X_test, y_test], axis=1)

        baseline_metrics = load_baseline_metrics(paths["reports"])
        if baseline_metrics:
            logging.info(f"Baseline metrics : {baseline_metrics}")

        mlflow.set_experiment("UBER_DVC_tuning")
        with mlflow.start_run(
            run_name="cat_model_optuna_tuning",
            description="Optuna multi-objective (recall & f1) tuning for CatBoost + SMOTE on the imbalanced dataset",
        ):
            study, best_trial = tune(params, X_train, y_train, args.n_trials, args.timeout, paths["tuning_study_db"])

            tuned_params = build_tuned_params(params, best_trial)
            metrics, cm, model, y_probs = retrain_and_evaluate(tuned_params, X_train, y_train, X_test, y_test)

            logging.info(f"Tuned model metrics on held-out test set : {metrics}")
            if baseline_metrics:
                logging.info(
                    f"Recall change : {baseline_metrics['recall']:.4f} -> {metrics['recall']:.4f} | "
                    f"F1 change : {baseline_metrics['f1_score']:.4f} -> {metrics['f1_score']:.4f} | "
                    f"PR-AUC : {baseline_metrics.get('pr_auc', 'n/a')} -> {metrics['pr_auc']:.4f}"
                )

            cm_to_heatmap(cm, paths["tuning_cm_path"])
            pr_curve_plot(y_test, y_probs, paths["tuning_pr_curve_path"])
            save_outputs(study, tuned_params, metrics, baseline_metrics, paths)
            log_final_run(
                model, metrics, tuned_params, best_trial, train_data, test_data,
                paths["params_path"], paths["tuning_cm_path"], paths["tuning_pr_curve_path"],
                X_train, X_test, paths["reports"],
            )

        logging.info("Hyperparameter tuning completed successfully")

    except Exception as e:
        logging.error(f"Tuning failed due to : {e}")
        raise e


if __name__ == "__main__":
    main()
