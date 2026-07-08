from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
import connection_manager
import inference

app = FastAPI()
manager = connection_manager.ConnectionManager()


@app.websocket("/chat")
async def chat(websocket: WebSocket, session_id: str = Query(...)):
    global manager
    await manager.connect(session_id, websocket)

    try:
        while True:
            user_message = await websocket.receive_text()

            if user_message == "/exit":
                await manager.send_message("Goodbye!", session_id)
                await websocket.close()
                break

            history = await manager.get_history(session_id)
            history.append({
                "role": "user",
                "content": user_message
            })

            stream = inference.ollama_response(history)
            response = ""

            async for chunk in stream:
                content = chunk.get('message', {}).get('content', "")
                if content:
                    response += content
                    await websocket.send_text(content)
            
            history.append({
                "role": "assistant",
                "content": response
            })

            await manager.set_conversation(session_id, history)

    except WebSocketDisconnect:
        await manager.disconnect(session_id)

    except KeyboardInterrupt:
        await manager.disconnect(session_id)
