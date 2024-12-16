from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import os
from fastapi.staticfiles import StaticFiles
app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/static')), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI server!"}

@app.get("/index")
def get_chart():
    file_path = os.path.join(os.path.dirname(__file__), '../frontend/index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@app.get("/data/{filename}")
def get_file(filename: str):
    return FileResponse(os.path.join("data", filename))

@app.get("/data/processed/{filename}")
def get_processed_file(filename: str):
    return FileResponse(os.path.join("data/processed", filename))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

