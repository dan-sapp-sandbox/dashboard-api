from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
import strawberry
import json
import random
import asyncio
from datetime import datetime, date, timedelta
from typing import List

# Load JSON data
def load_data(file_path: str = "api/scatterplot.json"):
    with open(file_path, "r") as file:
        return json.load(file)
    
# def generate_scatterplot_data(size, start, end):
#    return [{"x": random.randint(start, end), "y": random.randint(start, end)} for _ in range(size)]

# def generate_chart_data(num_points: int = 100, start_date: str = None):
#     if start_date is None:
#         start_date = datetime.today().strftime("%Y-%m-%d")
    
#     start = datetime.strptime(start_date, "%Y-%m-%d")
#     data = []

#     for i in range(num_points):
#         date = start + timedelta(days=i)
#         value = random.randint(20, 100)
#         data.append({"date": date.strftime("%Y-%m-%d"), "value": value})

#     return data

# Define GraphQL types
@strawberry.type
class ScatterPoint:
    x: int
    y: int
    
@strawberry.type
class AreaChartPoint:
    date: str
    value: str



@strawberry.type
class Query:
    @strawberry.field
    def scatterplot_data(self) -> List[ScatterPoint]:
        data = load_data("api/scatterplot.json")
        return [ScatterPoint(**point) for point in data["data"]]

    @strawberry.field
    def areachart_data(self) -> List[AreaChartPoint]:
        data = load_data("api/ice_cream_sales.json")
        return [
            AreaChartPoint(
                date=point["date"],
                value=point["value"]
            ) 
            for point in data
        ]

schema = strawberry.Schema(query=Query)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
  
# @app.get("/scatterplot-data")
# def read_root():
#     return {"data": generate_scatterplot_data(30, 0, 100)}
# @app.get("/areachart-data")
# def read_root():
#     return {"data": generate_chart_data(100)}
    
# @app.websocket("/ws/scatter")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             response = {"data": generate_scatterplot_data(50, 0, 100)}
#             await websocket.send_text(json.dumps(response))
#             await asyncio.sleep(5)
#     except WebSocketDisconnect:
#         print("Client disconnected")
        
# @app.websocket("/ws/area")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             response = {"data": generate_chart_data(100)}
#             await websocket.send_text(json.dumps(response))
#             await asyncio.sleep(5)
#     except WebSocketDisconnect:
#         print("Client disconnected")