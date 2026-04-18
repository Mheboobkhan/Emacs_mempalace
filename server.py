from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import subprocess
import requests
import time

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "" #add your model name here


# -------- Request Schema (gptel/OpenAI format) --------
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]


# -------- Memory Retrieval --------
def search_mempalace(query: str) -> str:
    try:
        result = subprocess.run(
            ["mempalace", "search", query],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"[ERROR] mempalace failed: {e}")
        return ""


# -------- Ollama Call --------
def ask_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        if response.status_code != 200:
            print("[ERROR] Ollama bad response:", response.text)
            return "Error: LLM request failed."

        data = response.json()
        return data.get("response", "")

    except Exception as e:
        print(f"[ERROR] Ollama request failed: {e}")
        return "Error: Unable to reach local model."


# -------- Main Endpoint --------
@app.post("/v1/chat/completions")
def chat(req: ChatRequest):
    try:
        # 🧠 Get latest user message
        user_prompt = req.messages[-1].content

        print(f"\n[REQUEST] {user_prompt}")

        # 🔎 Retrieve memory
        context = search_mempalace(user_prompt)

        # ⚡ Limit context size (important)
        context = context[:5000]

        # 🧩 Build final prompt
        full_prompt = f"""
You are a helpful assistant.

Use the context below to answer the question.
If context is not useful, answer normally.

CONTEXT:
{context}

QUESTION:
{user_prompt}

ANSWER:
"""

        # 🤖 Ask Ollama
        answer = ask_ollama(full_prompt)

        print(f"[RESPONSE] {answer[:200]}...\n")

        # ✅ OpenAI-compatible response (CRITICAL)
        return {
            "id": "chatcmpl-local",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": MODEL,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": answer
                    },
                    "finish_reason": "stop"
                }
            ]
        }

    except Exception as e:
        print(f"[FATAL ERROR] {e}")

        return {
            "id": "error",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": MODEL,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Internal server error."
                    },
                    "finish_reason": "stop"
                }
            ]
        }
