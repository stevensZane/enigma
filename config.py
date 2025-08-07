import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Optional: Raise error if any variable is missing
required_keys = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "ELEVENLABS_API_KEY": ELEVENLABS_API_KEY,
    "ELEVENLABS_VOICE_ID": ELEVENLABS_VOICE_ID,
    "OPENROUTER_API_KEY": OPENROUTER_API_KEY,
    "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY
}

for key, value in required_keys.items():
    if not value:
        raise ValueError(f"Missing environment variable: {key}")
