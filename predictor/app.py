from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
import joblib
import os
import pandas as pd
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()

class input_datatype(BaseModel):  # The Type of Data that user should enter. BaseModel is a pydantic model for dat validation
    Hours_Studied: int
    Attendance: int
    Extracurricular_Activities: str
    Sleep_Hours: int
    Previous_Scores: float


class ModelName(str, Enum):  # Not a pydantic model's instance
    linear = "LinearRegression"
    Lasso = "Lasso"
    Ridge = "Ridge"


@app.get("/")
async def root():  # async makes root() a coroutine, which can we stopped and presumed, dont wait for one task to complete
    return {"Welcome to Student Performance Prediction App"}


@app.post("/predict")
async def prediction(data: input_datatype, model: ModelName):
    if model.value == "LinearRegression":
        model_selected = os.getenv("LINEAR_MODEL_PATH")
    elif model.value == "Lasso":
        model_selected = os.getenv("LASSO_MODEL_PATH")
    else:
        model_selected = os.getenv("RIDGE_MODEL_PATH")

    # if  not os.path.exists(model_selected):
    #     raise HTTPException(status_code=500, detail=f"Model not found at {model_selected}")

    model_pipeline = joblib.load(model_selected)

    # Convert Pydantic model to dictionary (using Pydantic v2 syntax)
    sample = pd.DataFrame([data.model_dump()])

    try:
        prediction = model_pipeline.predict(sample)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "model_used": model.value,
        "predicted_score": round(float(prediction), 2),
        "input": data.model_dump(),
    }