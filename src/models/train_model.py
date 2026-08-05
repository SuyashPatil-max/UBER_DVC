import pandas as pd
import logging
from pathlib import Path
from sklearn.metrics import accuracy_score , confusion_matrix , precision_score , recall_score , roc_auc_score , f1_score
import pickle
import yaml
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.pipeline import Pipeline
from sklearn.utils import estimator_html_repr
import json
import mlflow 
import mlflow.sklearn
from imblearn.over_sampling import SMOTE
from mlflow.models.signature import infer_signature
import catboost as cat 
import dagshub
import os 


logging.basicConfig(
    level = logging.INFO , 
    format="%(asctime)s - %(name)s- %(levelname)s - %(message)s"
)


logging.info("Setting mlflow and dagshub : ")
mlflow.set_tracking_uri('https://dagshub.com/SuyashPatil-max/UBER_DVC')
dagshub.init(
    repo_owner = 'SuyashPatil-max' , 
    repo_name = 'UBER_DVC' ,
    mlflow = True 
)
token = os.getenv("DAGSHUB_TOKEN")
if token:
    dagshub.auth.add_app_token(token)
logging.info("Setting mlflow and dagshub finised ")


def load_paths() : 
    try : 
        paths = Path(__file__).resolve().parents[2]
        data_path = paths/'data'/'processed'

        try : 
            logging.info("Checking params paths...")
            params_path = paths/"params.yaml"
        except Exception as e : 
            logging.error(f"Params paths not found : {e}")
            raise e 

        return {
            'params_path' : params_path , 
            'X_train_path' : data_path /"X_train.csv",
            'X_test_path' : data_path /"X_test.csv",
            'y_train_path' : data_path /"y_train.csv",
            'y_test_path' : data_path /"y_test.csv"
        }

    except Exception as e : 
        logging.error(f"Error in loading paths : {e}")
        raise e 


def load_params(params_path) : 
    try : 
        logging.info("Loading params : ")
        with open(params_path , 'r') as f : 
            params = yaml.load_safe(f) 

        return params 

    except Exception as e : 
        logging.error(f"params not loaded ") 
        raise e 


def train_model(X_train ,y_train ,params) : 
    try : 
        logging.info("Setting pipeline : ")

        cat_params = params['cat_model']
        smote_params = params['smote']
        model = Pipeline([
            ('smote', SMOTE(**smote_params)),
            ('catboost', cat.CatBoostClassifier(**cat_params))
        ])

        logging.info("Training started : ")
        model.fit(X_train,y_train)
        logging.info("Training completed")

        return model

    except Exception as e : 
        logging.error(f"Training model failed : ")
        raise e 


def eval_model(model) : 
    pass 


def ml() : 
    pass 


def save_model():
    pass


def main() : 
    pass 


if __name__ == "__main__" : 
    main()