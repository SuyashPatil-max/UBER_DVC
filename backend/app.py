from fastapi import FastAPI ,HTTPException
from fastapi.responses import JSONResponse 
from .schema.valid_in import Ride_IN
from .predict import predict_output ,load_models
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path as pt 
import pandas as pd 
import pickle
import json

    
def load_model_version() : 
    paths = pt(__file__).resolve().parents[1]/"reports"/"model_version.json"
    with open(paths , 'r') as f : 
        version = json.load(f)

    return version


app = FastAPI(
    title = "Uber ride prediction API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


@app.post('/predict')
def predict_ride(data : Ride_IN) : 
    input_data = {
    "Vehicle Type": data.vehicle_type.value,
    "Pickup Location": data.pickup_location.value,
    "Drop Location": data.drop_location.value,

    "Avg VTAT": data.vtat,
    "Avg CTAT": data.ctat,
    "Booking Value": data.Booking_value,
    "Ride Distance": data.Ride_Distance,

    "Payment Method": data.payment_method.value,

    "Month": data.Month,
    "Day": data.Day,
    "DayOfWeek": data.DayOfWeek,
    "Quarter": data.Quarter,
    "IsWeekend": data.IsWeekend,
    "Hour": data.Hour,
    "TimeOfDay": data.TimeOfDay,
    "Season": data.Season
    }

    output = predict_output(input_data)
    return output 


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8002,
    )
