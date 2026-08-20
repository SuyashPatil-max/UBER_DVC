import json
import os
import logging

import dagshub
import mlflow
from dotenv import load_dotenv
from mlflow import MlflowClient

load_dotenv()

token = os.getenv("DAGSHUB_TOKEN")

if token:
    dagshub.auth.add_app_token(token)

dagshub.init(
    repo_owner="SuyashPatil-max",
    repo_name="UBER_DVC",
    mlflow=True,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

MODEL_NAME = "uber"

def load_model_info():
    with open("reports/experiment.json", "r") as f:
        return json.load(f)


def register_model():
    model_info = load_model_info()

    registered_model = mlflow.register_model(
        model_uri=model_info["model_uri"],
        name=MODEL_NAME,
    )

    client = MlflowClient()

    client.set_registered_model_alias(
        name=MODEL_NAME,
        alias="champion",
        version=registered_model.version,
    )

    logger.info(f"Model registered successfully.")
    logger.info(f"Version : {registered_model.version}")

    return registered_model.version


def main():
    version = register_model()
    print(f"Registered Version : {version}")


if __name__ == "__main__":
    main()