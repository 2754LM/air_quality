from asyncio import sleep
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from backend.processing import pollution_all
from backend.processing import pollutants_statistics
from backend.processing import aqi_ranges



app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/static')), name="static")

@app.get("/")
def get_chart():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@app.get("/data/{filename}")
def get_file(filename: str):
    return FileResponse(os.path.join("data", filename))

@app.get("/data/processed/{filename}")
def get_processed_file(filename: str):
    return FileResponse(os.path.join("data", "processed", filename))

@app.post("/update_all")
async def update_info():
    await sleep(1) #测试用的，正式调用把下面参数传true
    pollution_all.pollution_all()
    aqi_ranges.aqi_ranges()
    pollutants_statistics.pollutant_statistics()
