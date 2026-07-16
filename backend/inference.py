from typing import List, Dict
import ollama

MODEL = "qwen3.5:2b"

def ollama_response(conversation_history: List[Dict[str, str]]):
    response = ollama.chat(MODEL, messages=conversation_history, think=False, stream=False)
    return response['message']['content']

if __name__ == "__main__":
    print(ollama_response([{
        "role": "user",
        "content": "Why is the sky blue?"
    }]))