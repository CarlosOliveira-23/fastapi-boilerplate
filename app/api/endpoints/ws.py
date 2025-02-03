from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

active_connections: List[WebSocket] = []


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await broadcast_message(f"Nova mensagem recebida: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)


async def broadcast_message(message: str):
    """Envia a mensagem para todos os clientes conectados."""
    for connection in active_connections:
        await connection.send_text(message)
