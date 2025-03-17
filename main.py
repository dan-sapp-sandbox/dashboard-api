from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import asyncio
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"], 
    allow_headers = ["*"], 
)

def generate_scatterplot_data(size, start, end):
   return [{"x": random.randint(start, end), "y": random.randint(start, end)} for _ in range(size)]

def generate_chart_data(num_points: int = 100, start_date: str = None):
    if start_date is None:
        start_date = datetime.today().strftime("%Y-%m-%d")
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    data = []

    for i in range(num_points):
        date = start + timedelta(days=i)
        value = random.randint(20, 100)
        data.append({"date": date.strftime("%Y-%m-%d"), "value": value})

    return data

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
  
@app.get("/data")
def read_root():
    return {
      "data": generate_scatterplot_data(30, 0, 100)
    }
    
@app.websocket("/ws/scatter")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            response = {"data": generate_scatterplot_data(50, 0, 100)}
            await websocket.send_text(json.dumps(response))
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected")
        
@app.websocket("/ws/area")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            response = {"data": generate_chart_data(100)}
            await websocket.send_text(json.dumps(response))
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        print("Client disconnected")