from dotenv import load_dotenv
load_dotenv()
import os
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("Models available to this API key:")
for m in client.models.list():
    print(" -", m.name)