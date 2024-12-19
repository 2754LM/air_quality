import sys
import os

from pydantic import BaseModel # pylint: disable=no-name-in-module

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from backend.processing import control

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/static')), name="static")

@app.get("/")
def get_chart():
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