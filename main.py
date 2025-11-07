from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from passlib.hash import bcrypt 

app = FastAPI()

MONGO_URL = "mongodb+srv://echo_user:Ocha0401@escape-of-echo.7d0wroy.mongodb.net/?appName=escape-of-echo"
client = MongoClient(MONGO_URL)

db = client["escape_of_echo_db"]
players = db["players"]

class PlayerCreate(BaseModel):
    username: str
    password: str

@app.post("/player/register")
def register_player(player: PlayerCreate):
   hashed_password = bcrypt.hash(player.password)
   players.insert_one({
       "username": player.username,
       "password": hashed_password
   })
   return {"message": "登録完了！"," username": player.username}



class RegisterUser(BaseModel):
    username: str
    password: str 

@app.post("/player/register")
def register_user(user:RegisterUser):
    if players.find_one({"username": user.username}):
        return {"error": "Username already exists"}
    hashed_pw = bcrypt.hash(user.password)
    players.insert_one({"username": user.username, "password": hashed_pw})
    return {"message": "User registered successfully"}


@app.get("/testdb")
def test_db():
    test_data = {"name": "test_user", "status": "MongoDB connected!"}
    result = players.insert_one(test_data)
    return {"message": "Inserted", "id": str(result.inserted_id)}
