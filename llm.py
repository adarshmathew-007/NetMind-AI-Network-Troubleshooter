import os
import sys

try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from google import genai
from google.genai import types

MODEL_CANDIDATES = ["gemini-3.8-flash"]

_chosen_model = None
client = None


def _get_api_key():
    try:
        import config
        key = getattr(config, "GEMINI_API_KEY", None)
        if key:
            return key
    except ImportError:
        pass
    return os.environ.get("GEMINI_API_KEY")


def _get_client():
    global client
    if client is not None:
        return client

    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError("No Gemini model available: GEMINI_API_KEY is not set")

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=10_000,
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )
    return client


def _pick_model():
    """
    Iterate through MODEL_CANDIDATES and return the first working model name.
    Caches the chosen model in a module-level variable.
    """
    global _chosen_model
    if _chosen_model is not None:
        return _chosen_model

    c = _get_client()

    for model in MODEL_CANDIDATES:
        try:
            c.interactions.create(
                model=model,
                input="ping",
            )
            _chosen_model = model
            print(f"[NetMind] Using Gemini model: {model}", flush=True)
            return _chosen_model
        except Exception:
            continue

    raise RuntimeError("No Gemini model available")


def call_llm(history):
    """
    Send the agent conversation to Gemini and return the reply text.
    """
    model = _pick_model()
    c = _get_client()

    prompt = ""
    for message in history:
        prompt += f"{message['role']}: {message['content']}\n"

    interaction = c.interactions.create(
        model=model,
        input=prompt,
    )

    return interaction.output_text