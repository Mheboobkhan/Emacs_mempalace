import subprocess
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"   # ✅ corrected


def search_mempalace(query):
    try:
        result = subprocess.run(
            ["mempalace", "search", query],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] mempalace failed: {e}")
        return ""


def ask_ollama(question, context):
    prompt = f"""
You are a helpful assistant. Use the context to answer.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        # ✅ Debug visibility
        if response.status_code != 200:
            print("[ERROR] Bad response:", response.text)
            return "LLM request failed."

        data = response.json()

        # ✅ Safe parsing
        return data.get("response", "[No response field found]")

    except requests.exceptions.RequestException as e:
        return f"[ERROR] Request failed: {e}"


def main():
    print("🔐 Local Assistant (type 'exit' to quit)\n")

    while True:
        question = input(">> ")

        if question.lower() in ["exit", "quit"]:
            break

        context = search_mempalace(question)

        answer = ask_ollama(question, context)

        print("\n🧠 Answer:\n")
        print(answer)
        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()
