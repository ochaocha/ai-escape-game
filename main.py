from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

MONGO_URL = "mongodb+srv://echo_user:Ocha0401@escape-of-echo.7d0wroy.mongodb.net/?appName=escape-of-echo"
client = MongoClient(MONGO_URL)

db = client["escape_of_echo_db"]
players = db["players"]

@app.get("/testdb")
def test_db():
    test_data = {"name": "test_user", "status": "MongoDB connected!"}
    result = players.insert_one(test_data)
    return {"message": "Inserted", "id": str(result.inserted_id)}
