from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import base64
from PIL import Image
from io import BytesIO

from model import MLModel

model = MLModel()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

IMAGE_SIZE = 224

@app.post("/")
async def process_image(base64_image: str = Form(...)):
    decoded_image_data = base64.b64decode(base64_image)
    image = Image.open(BytesIO(decoded_image_data))
    resized_image = image.resize((IMAGE_SIZE, IMAGE_SIZE))
    breed = model_response(resized_image)
    return {"breed": breed}

def model_response(resized_image: Image.Image) -> str:
    # feed image into model
    # return model response for breed type
    return model.predict(resized_image)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
