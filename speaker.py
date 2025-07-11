# speaker.py

import requests
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID

def speak(text):
    print(f"🧠 Responding: {text}")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }

    response = requests.post(url, json=data, headers=headers)
    if response.ok:
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        try:
            import playsound
            playsound.playsound("output.mp3")
        except Exception as e:
            print(f"Error playing audio: {e}")
    else:
        print(f"Error from ElevenLabs: {response.text}")
