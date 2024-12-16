from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import os
import json  # 导入 json 模块
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/static')), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/test")
def get_test_data():
    file_path =  os.path.join(os.path.dirname(__file__), 'data/processed/test.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f) 
    return JSONResponse(content=content)

@app.get("/index")
def get_chart():
    file_path = os.path.join(os.path.dirname(__file__), '../frontend/index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

