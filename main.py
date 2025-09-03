from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def get_root():
    return FileResponse('index.html')

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        print(f"Broadcasting: {message}")
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    print(f"Client #{client_id} connected. Total clients: {len(manager.active_connections)}")
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received from #{client_id}: {data}")
            if data.startswith("typing:"):
                # Typing status, broadcast to other users
                for connection in manager.active_connections:
                    if connection != websocket:
                        await connection.send_text(f"{client_id}:{data}")
            else:
                # Regular chat message
                await manager.broadcast(f"{client_id}:{data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"Client #{client_id} disconnected.")
