import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

models_to_try = [
    "gemini-3.8-flash",
    "gemini-3.5-flash",
    "gemini-2.5-flash",
    "gemini-3.1-flash-lite",
]

for name in models_to_try:
    try:
        interaction = client.interactions.create(
            model=name,
            input="Reply with just the word: OK",
        )
        print(f"✅ {name}  →  {interaction.output_text.strip()!r}", flush=True)
    except Exception as e:
        print(f"❌ {name}  →  {type(e).__name__}: {str(e)[:120]}", flush=True)