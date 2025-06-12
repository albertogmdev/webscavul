from fastapi import FastAPI
import app.modules.headers as headers

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/headers")
def analyze_headers(url: str):
    result = headers.analyze_headers(url)
    return result

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}