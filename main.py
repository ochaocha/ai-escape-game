from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from passlib.hash import bcrypt 

#Steam APIキー
STEAM_API_KEY = "YOUR_STEAM_API_KEY"   
STEAM_API_URL = "http://api.steampowered.com" 

#ファストAPIのインスタンスの作成
app = FastAPI()

#mongoDBの接続設定
MONGO_URL = "mongodb+srv://echo_user:Ocha0401@escape-of-echo.7d0wroy.mongodb.net/?appName=escape-of-echo"
client = MongoClient(MONGO_URL)

#クライアントからの階層をDBという変数に入れている
db = client["escape_of_echo_db"]
players = db["players"]

#ベースモデルからの継承したもの
class PlayerCreate(BaseModel):
    username: str 
    passward: str


#postは関数修飾子　def自体は関数定義
@app.post("/player/register")
def register_player(player: PlayerCreate):
   hashed_password = bcrypt.hash(player.password)
   players.insert_one({
       "username": player.username,
       "password": hashed_password
   })
   return {"message": "登録完了！"," username": player.username}

#ベースモデルの継承
class RegisterUser(BaseModel):
    username: str
    password: str 

#appから持ってきたpostapi関数
@app.post("/player/register")
def register_user(user:RegisterUser):
    if players.find_one({"username": user.username}):
        return {"error": "Username already exists"}
    hashed_pw = bcrypt.hash(user.password)
    players.insert_one({"username": user.username, "password": hashed_pw})
    return {"message": "User registered successfully"}

#テスト用のデータベースの関数
@app.get("/testdb")
def test_db():
    test_data = {"name": "test_user", "status": "MongoDB connected!"}
    result = players.insert_one(test_data)
    return {"message": "Inserted", "id": str(result.inserted_id)}


