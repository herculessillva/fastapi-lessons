from fastapi import FastAPI
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import get_file, load_img, img_to_array
from tensorflow import expand_dims
from tensorflow.nn import softmax
from numpy import argmax, max
from json import dumps
from uvicorn import run
import os
from utils import class_predictions

app = FastAPI()
model_dir = "food-vision-model.h5"
model = load_model(model_dir)

@app.post("/net/image/prediction/")
async def get_net_image_prediction(image_link: str = ""):
    if image_link == "":
        return {"message": "No image link provided"}
    
    img_path = get_file(
        origin = image_link
    )
    img = load_img(
        img_path, 
        target_size = (224, 224)
    )

    img_array = img_to_array(img)
    img_array = expand_dims(img_array, 0)

    pred = model.predict(img_array)
    score = softmax(pred[0])

    class_prediction = class_predictions[argmax(score)]
    model_score = round(max(score) * 100, 2)

    return {
        "model-prediction": class_prediction,
        "model-prediction-confidence-score": model_score
    }