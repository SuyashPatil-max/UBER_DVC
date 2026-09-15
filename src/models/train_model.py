import pandas as pd
import numpy as np
import logging
from pathlib import Path
from sklearn.metrics import (
    confusion_matrix , precision_score , recall_score , roc_auc_score , f1_score,
    average_precision_score, balanced_accuracy_score, matthews_corrcoef, precision_recall_curve
)
import pickle
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.pipeline import Pipeline
# from sklearn.utils import estimator_html_repr
import json
import mlflow 
import mlflow.sklearn
from imblearn.over_sampling import SMOTE,SMOTENC
from mlflow.models.signature import infer_signature
import catboost as cat 
import dagshub
import os 


logging.basicConfig(
    level = logging.INFO , 
    format="%(asctime)s - %(name)s- %(levelname)s - %(message)s"
)


logging.info("Setting mlflow and dagshub : ")

token = os.getenv("DAGSHUB_TOKEN")
if token:
    dagshub.auth.add_app_token(token)

mlflow.set_tracking_uri("https://dagshub.com/SuyashPatil-max/UBER_DVC.mlflow")
dagshub.init(
    repo_owner = 'SuyashPatil-max' , 
    repo_name = 'UBER_DVC' ,
    mlflow = True 
)
logging.info("Setting mlflow and dagshub finised ")


def load_paths() : 
    try : 
        paths = Path(__file__).resolve().parents[2]
        data_path = paths/'data'/'processed'
        models = paths/"models"
        cm_path = paths/"reports"/'cm.png'
        pr_curve_path = paths/"reports"/'pr_curve.png'
        reports_path = paths/"reports"

        try : 
            logging.info("Checking params paths...")
            params_path = paths/"params.yaml"
        except Exception as e : 
            logging.error(f"Params paths not found : {e}")
            raise e 

        return {
            'reports' : reports_path ,
            'cm_path' : cm_path,
            'pr_curve_path' : pr_curve_path,
            'models' : models,
            'params_path' : params_path , 
            'X_train_path' : data_path /"X_train.csv",
            'X_test_path' : data_path /"X_test.csv",
            'y_train_path' : data_path /"y_train.csv",
            'y_test_path' : data_path /"y_test.csv"
        }

    except Exception as e : 
        logging.error(f"Error in loading paths : {e}")
        raise e 


def load_data(data_path : str ) -> pd.DataFrame : 
    try : 
        logging.info(f"Loading {data_path} dataset")
        return pd.read_csv(data_path)

    except Exception as e : 
        logging.error(f"Error in loading {data_path} dataset")
    

def load_params(params_path) : 
    try : 
        logging.info("Loading params : ")
        with open(params_path , 'r') as f : 
            params = yaml.safe_load(f) 

        return params 

    except Exception as e : 
        logging.error(f"params not loaded ") 
        raise e 


def train_models(X_train ,y_train ,params) : 
    try : 

        logging.info("Setting pipeline : ")

        cat_params = params['cat_model']
        smote_params = params['smote']

        model = Pipeline([
            ('smote', SMOTE(**smote_params)),
            ('catboost', cat.CatBoostClassifier(**cat_params))
        ])

        logging.info("Training started : ")
        model.fit(X_train,y_train )
        logging.info("Training completed")

        return model

    except Exception as e : 
        logging.error(f"Training model failed : ")
        raise e 


def eval_model(model , X_test ,y_test) :
    # NOTE on why both roc_auc and pr_auc are computed:
    # this is a ~10:1 imbalanced problem (Completed vs Incomplete), and ROC-AUC
    # is computed against the large, easy-to-separate negative class, so it
    # stays high almost regardless of how well the model does on the positive
    # (minority) class. PR-AUC (average precision) only scores the positive
    # class and is far more honest here. balanced_accuracy and MCC are added
    # for the same reason: plain accuracy would be dominated by the majority
    # class, these two are not.
    try :
        logging.info("Evaluation of model starting : ")
        y_pred = model.predict(X_test)
        y_probs = model.predict_proba(X_test)[:, -1]
        y_true = np.asarray(y_test).ravel()

        metrics =  {
            'recall' : recall_score(y_true , y_pred),
            'precision' : precision_score(y_true ,y_pred) ,
            'f1_score' : f1_score(y_true ,y_pred),
            'roc_auc' : roc_auc_score(y_true , y_probs),
            'pr_auc' : average_precision_score(y_true , y_probs),
            'balanced_accuracy' : balanced_accuracy_score(y_true , y_pred),
            'mcc' : matthews_corrcoef(y_true , y_pred),
            'positive_class_prevalence' : float(y_true.mean())
        }
        cm = confusion_matrix(y_true, y_pred)
        logging.info("Evaluation of model completed : ")
        return metrics ,cm ,y_probs
    except Exception as e :
        logging.error("Error in the evalution of model ")
        raise e


def cm_to_heatmap(cm , cm_path) :
    try :
        logging.info(f"Saving the cm to {cm_path}")
        plt.figure(figsize = (12,8))
        sns.heatmap(cm , cmap = 'Blues' , annot = True , fmt = 'd')
        plt.savefig(cm_path , dpi = 300 , bbox_inches ='tight')
        plt.close()

    except Exception as e :
        logging.error("Error occured in saving cm ")
        raise e


def pr_curve_plot(y_test, y_probs, pr_curve_path):
    # A random/no-skill classifier's PR curve is a flat line at the positive
    # class prevalence, not at 0.5 like ROC's diagonal - plotting that
    # baseline alongside the real curve is what makes pr_auc interpretable.
    try:
        logging.info(f"Saving the PR curve to {pr_curve_path}")
        y_true = np.asarray(y_test).ravel()
        precision, recall, _ = precision_recall_curve(y_true, y_probs)
        baseline = y_true.mean()

        plt.figure(figsize=(10, 7))
        plt.plot(recall, precision, label="CatBoost + SMOTE")
        plt.axhline(baseline, color="grey", linestyle="--",
                    label=f"Random baseline (prevalence = {baseline:.3f})")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title("Precision-Recall curve (positive class = Incomplete)")
        plt.legend()
        plt.savefig(pr_curve_path, dpi=300, bbox_inches="tight")
        plt.close()

    except Exception as e:
        logging.error("Error occured in saving pr curve ")
        raise e 

def ml(model, metrics, params, train_data, test_data ,params_path ,cm_path, pr_curve_path, X_train, X_test, reports_path) :
    try : 
        logging.info("Starting MLFLOW ")
        mlflow.set_experiment('UBER_DVC')

        cat_params = {
            f"catboost_{k}": v
            for k, v in params["cat_model"].items()
                }
        smote_params = {
            f"smote_{k}": v
            for k, v in params["smote"].items()
                }
        with mlflow.start_run(run_name = 'Best Model',description="ordinal encoding") as run : 
            mlflow.log_metrics(metrics)
            mlflow.log_params(cat_params)
            mlflow.log_params(smote_params)

            train_data = mlflow.data.from_pandas(train_data)
            test_data = mlflow.data.from_pandas(test_data)
            mlflow.log_input(train_data, context = "train_data")
            mlflow.log_input(test_data , context = "test_data")

            mlflow.log_artifact(params_path)
            mlflow.log_artifact(cm_path)
            mlflow.log_artifact(pr_curve_path)

            sig = infer_signature(X_train ,model.predict(X_test))
            model_info = mlflow.sklearn.log_model(model ,
                                                  "cat_smote_model",
                                                  signature = sig,
                                                serialization_format="pickle"
                                                )

            with open(reports_path/"experiment.json" , 'w') as f : 
                json.dump(
                    {
                        'run_id' : run.info.run_id ,
                        'model_uri' : model_info.model_uri
                    }, f 
                )
            logging.info("Logging of all things in ml completed : ")

    except Exception as e : 
        logging.error("Error in the mlflow ")
        raise e  
    

def save_model(model, metrics, model_path, reports_path):
    try : 
        logging.info("Saving model and metrics : ")
        with open(model_path ,'wb') as f : 
            pickle.dump(model ,f )

        with open(reports_path/"metrics.json",'w') as f :
            json.dump(metrics ,f,indent =4  )
        logging.info("Model and metrics saved successfully")

    except Exception as e : 
        logging.error("Error in saving model and metrics ")
        raise e 


def main() : 
    try : 
        logging.info("starting the main ")
        path = load_paths()

        reports_path =path['reports']
        cm_path = path['cm_path']
        pr_curve_path = path['pr_curve_path']
        models_path = path['models']
        X_train_path =path['X_train_path']
        y_train_path =path['y_train_path']
        X_test_path =path['X_test_path']
        y_test_path =path['y_test_path']
        params_path =path['params_path']

        params = load_params(params_path)

        X_train = load_data(X_train_path)
        X_test = load_data(X_test_path)
        y_train = load_data(y_train_path)
        y_test =load_data(y_test_path)

        train_data = pd.concat([X_train , y_train] , axis = 1 ) 
        test_data = pd.concat([X_test ,y_test] , axis = 1)

        model = train_models(X_train ,y_train ,params)
        metrics ,cm ,y_probs = eval_model(model , X_test ,y_test)
        cm_to_heatmap(cm , cm_path)
        pr_curve_plot(y_test, y_probs, pr_curve_path)
        save_model(model, metrics ,models_path/"model.pkl" ,reports_path)
        ml(model, metrics, params, train_data, test_data ,params_path ,cm_path, pr_curve_path, X_train, X_test, reports_path)
        
        logging.info("Main is completed without error")
        
    except Exception as e : 
        logging.error(f"Error in main {e}") 
        raise e 
    

if __name__ == "__main__" : 
    main()