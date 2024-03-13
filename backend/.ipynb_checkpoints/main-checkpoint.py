from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/answer/{image_id}")
def get_model_answer(image_id: int, q: str = None):
    answer = "cat"
    return {"answer": answer, "q": q}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
