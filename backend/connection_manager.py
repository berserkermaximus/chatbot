from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

    async def connect(self, session_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[session_id] = websocket
        if session_id not in self.sessions:
            self.sessions[session_id] = [
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant."
                }
            ]

    async def get_history(self, session_id: str):
        if self.sessions[session_id]:
            return self.sessions[session_id]
        else:
            return None
        
    async def set_conversation(self, session_id: str, history: List[Dict[str, str]]):
        self.sessions[session_id] = history

    async def send_message(self, session_id: str, response: str):
        if self.connections.get(session_id):
            await self.connections[session_id].send_text(response)
            

    async def disconnect(self, session_id: str):
        if session_id in self.connections:
            del self.connections[session_id]
            del self.sessions[session_id]
