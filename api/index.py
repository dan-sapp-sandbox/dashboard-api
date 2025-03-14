from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"], 
    allow_headers = ["*"], 
)

def generate_random_numbers(size, start, end):
   return [{"x": random.randint(start, end), "y": random.randint(start, end)} for _ in range(size)]

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
  
@app.get("/data")
def read_root():
    return {
      "data": generate_random_numbers(30, 0, 100)
    }
    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = {"data": generate_random_numbers(30, 0, 100)}
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("Client disconnected")