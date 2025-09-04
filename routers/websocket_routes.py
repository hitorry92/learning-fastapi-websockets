from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from connection_manager import ConnectionManager

router = APIRouter()

# 1. 애플리케이션 전체에서 사용할 단일 ConnectionManager 인스턴스를 생성합니다.
manager = ConnectionManager()


# 2. 생성된 단일 인스턴스를 반환하는 의존성 함수를 정의합니다.
def get_manager() -> ConnectionManager:
    return manager


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    manager: ConnectionManager = Depends(get_manager),
):
    await manager.connect(websocket)
    print(
        f"Client #{client_id} connected. Total clients: {len(manager.active_connections)}"
    )
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
