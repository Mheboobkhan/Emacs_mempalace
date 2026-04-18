# 🧠 Designing a Private AI with Memory in Emacs — No Cloud, for $0

A fully local, private AI assistant with persistent memory, built using:

- **Ollama** → runs LLM locally  
- **MemPalace** → provides long-term memory  
- **Emacs (gptel)** → user interface  
- **FastAPI/Uvicorn** → middleware layer  

No cloud. No API keys. Zero cost.

---

## 🚀 What is this?

This project turns a stateless LLM into a **stateful second brain**.

Instead of answering each prompt in isolation, the system:
1. Retrieves relevant memory from your notes (MemPalace)
2. Injects it into the prompt
3. Sends it to the LLM (Ollama)
4. Returns a context-aware response in Emacs



---

## ✨ Features

- 🔐 100% local & private  
- 🧠 Persistent memory (semantic retrieval)  
- ⚡ Fast local inference (Ollama)  
- 📝 Emacs-native workflow (gptel)  
- 💡 Ideal for vibe coding, note-taking, and research  

---

## 🧱 Architecture


User (Emacs)
->
gptel (client)
->
FastAPI / Uvicorn (middleware)
->
MemPalace (memory retrieval)
->
Ollama (LLM)
->
Response back to Emacs



---

## ⚙️ Setup

### 1. Install Ollama

```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
```
### 2. Setup MemPalace
```
conda create -n mempalace python=3.11 -y
conda activate mempalace
pip install mempalace

mempalace init <your-notes-directory>
mempalace mine  <your-notes-directory>
```

### 3. Run Middleware Server 
```
pip install fastapi uvicorn
uvicorn server:app --port 8000 --http h11
```

### 4. Emacs config 
```
(use-package gptel
  :config
  (setq gptel-backend
        (gptel-make-openai "Local-RAG"
          :host "http://localhost:8000"
          :endpoint "/v1/chat/completions"
          :stream nil
          :key "dummy"))
  (setq gptel-model "llama3.1:8b"))
```

💡 Vibe Coding Use Case

This setup shines in vibe coding.

Instead of repeating context:

The system remembers your code patterns
Recalls past decisions
Connects notes with implementation

