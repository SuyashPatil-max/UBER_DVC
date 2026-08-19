from fastapi import FastAPI ,HTTPException
from fastapi.responses import JSONResponse 
from .schema import prediction_input
from .schema import prediction_output 
from .preprocessing import Date_time
from pathlib import Path as pt 


path = pt(__file__).resolve().parents[1]
def paths() : 
    models_path = path/"models"
    le_path = models_path/"le.pkl"
    model_path =models_path/"model.pkl"
    ohe_path = models_path/"ohe.pkl"
    trf_path = models_path/"trf.pkl"

    return {
        "model" : model_path,
        "trf" : trf_path,
        "ohe" : ohe_path, 
        "le" : le_path
    }


def load_models():
    pass



app = FastAPI(
    title = "Uber ride prediction API"
)

@app.get('/')
def home_page():
    return {
        "result" : "Welcome to uber ride prediction model"
    }


@app.get('/health')
def health_page():
    return { 
        "result" : "ok"
    }