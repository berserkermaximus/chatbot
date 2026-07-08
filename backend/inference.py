from typing import List, Dict
import ollama

MODEL = "qwen3.5:2b"

async def ollama_response(conversation_history: List[Dict[str, str]]):
    response = ollama.chat(MODEL, messages=conversation_history, think=False, stream=True)
    for chunk in response:
        yield chunk