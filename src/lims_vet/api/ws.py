import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Any

from ..core.pubsub import broker

router = APIRouter(tags=["websocket"])

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Callback that gets triggered on pubsub events
    async def pubsub_callback(message: Dict[str, Any]):
        try:
            await websocket.send_json(message)
        except Exception:
            pass # Ignore errors on send

    # Subscribe to events topic
    broker.subscribe("events", pubsub_callback)

    try:
        while True:
            # Just keep connection open and listen
            data = await websocket.receive_text()
            # Optionally handle client messages
    except WebSocketDisconnect:
        pass
    finally:
        broker.unsubscribe("events", pubsub_callback)
