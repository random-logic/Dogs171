from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import base64
from PIL import Image
from io import BytesIO

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.post("/")
async def process_image(base64_image: str = Form(...)):
    # Decode the Base64-encoded image data
    decoded_image_data = base64.b64decode(base64_image)

    image = Image.open(BytesIO(decoded_image_data))
    return {"breed": "doggy"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
