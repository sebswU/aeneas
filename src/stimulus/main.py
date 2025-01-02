from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

#------------REST API Stuff-------------------------------------

"""
These are active when the FastAPI server is called. 
"""

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json(mode='text')
        await websocket.send_text(f"Message text was: {data["ls"][4]}")

#---------------Basic Websocket Comms---------------------------
        


