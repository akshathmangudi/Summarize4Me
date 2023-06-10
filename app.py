from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from Summarize4Me.pipeline.prediction import PredictionPipeline
import uvicorn
import os
import sys


text:str = "What is Text Summarization?"
app = FastAPI()


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful.")

    except Exception as e:
        return Response(f"Error occured: {e}")


@app.post("/predict")
async def predict(text):
    try:
        text = PredictionPipeline().predict(text)
        return text
    except Exception as e:
        raise e

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)