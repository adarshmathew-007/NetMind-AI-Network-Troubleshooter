import requests
import json

def call_llm(history):
    """
    Send the agent conversation to the local Ollama instance.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3.2:3b",
                "messages": history,
                "stream": False,
                "format": "json"  # Forces Ollama to return valid JSON
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
    
    except requests.exceptions.ConnectionError:
        raise RuntimeError("Ollama is not running. Start the Ollama app.")
    except Exception as e:
        raise RuntimeError(f"Ollama error: {e}")
