from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# ① トップページ（確認用）
@app.get("/")
def read_root():
    return {"message": "AI Escape Game Server is running!"}

# ② Queryパラメータの例（/hello?name=ocha）
@app.get("/hello")
def say_hello(name: str = "world"):
    return {"message": f"Hello, {name}!"}

# ③ JSONデータを受け取る型（POST用）
class Item(BaseModel):
    name: str
    description: str

# ④ POST API（/item）
@app.post("/item")
def create_item(item: Item):
    return {"received": item}
