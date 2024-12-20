import sys
import os
from pydantic import BaseModel
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from fastapi import  FastAPI, HTTPException, Header
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from backend.processing import control
from backend import mysql,token_manger

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/static')), name="static")

@app.get("/")
def get_chart():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'login.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

class LoginInfo(BaseModel):
    username: str
    password: str
    rember: str
@app.post("/login")
def login(info : LoginInfo):
    if mysql.check_user(info.username,info.password):
        token = token_manger.create_access_token(data={"username": info.username, "password": info.password}, timeout = int(info.rember))
        return {'token': token}
    else:
        raise HTTPException(status_code=401, detail="用户名或密码错误")

@app.post("/register")
def register(info : LoginInfo):
    if mysql.check_exist(info.username):
        raise HTTPException(status_code=401, detail="用户名已存在")
    else:
        mysql.add_user(info.username,info.password)
        return {'message': '注册成功'}

    
@app.get("/protected")
async def read_protected(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="无效的凭证")
    token = authorization
    if token_manger.decode_jwt(token) == None:
        raise HTTPException(status_code=401, detail="无效的凭证")
    file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@app.get("/data/{filename}")
def get_file(filename):
    return FileResponse(os.path.join("data", filename))

@app.get("/data/processed/{filename}")
def get_processed_file(filename):
    return FileResponse(os.path.join("data", "processed", filename))


class UpdateInfo(BaseModel):
    province_name: str
    history: str

@app.post("/latest")
async def check_latest(info: UpdateInfo):
    if control.check_latest(info.province_name, info.history):
        return {'flag': 'true'}
    return {'flag' : 'false'}


@app.post("/update")
async def update_info(info: UpdateInfo):
    control.update_data(info.province_name, info.history)
    return {"province_name": info.province_name}
