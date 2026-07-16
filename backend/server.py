from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
import connection_manager
import inference
import asyncio
from messaging_queue import queue

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

            print(history)

            job = queue.enqueue(inference.ollama_response, history)

            while job.result is None:
                job.refresh()
                await asyncio.sleep(0.5)

            response = job.result

            # response = inference.ollama_response(history)
            
            history.append({
                "role": "assistant",
                "content": response
            })

            print(history)

            await manager.set_conversation(session_id, history)

            await websocket.send_text(response)

    except WebSocketDisconnect:
        await manager.disconnect(session_id)

    except KeyboardInterrupt:
        await manager.disconnect(session_id)
