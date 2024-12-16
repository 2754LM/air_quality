from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import os
import json  # 导入 json 模块

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/test")
async def get_test_data():
    file_path =  os.path.join(os.path.dirname(__file__), 'data/processed/test.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f) 
    return JSONResponse(content=content)

@app.get("/chart")
async def get_chart():
    file_path = os.path.join(os.path.dirname(__file__), '../frontend/test.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
