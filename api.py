from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import tensorflow as tf
from PIL import Image
import numpy as np
import uvicorn

app = FastAPI()
model = tf.keras.models.load_model("models/crop_disease_model.h5")
classes = ["Healthy", "Disease1", "Disease2"]  # Replace with actual class names

def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    return np.expand_dims(image, axis=0)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = Image.open(file.file)
    input_data = preprocess_image(image)
    predictions = model.predict(input_data)
    class_id = np.argmax(predictions)
    confidence = predictions[0][class_id]
    return JSONResponse(content={
        "class": classes[class_id],
        "confidence": float(confidence)
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
