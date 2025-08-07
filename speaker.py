import socket
import requests
import os
import time
import pygame
from gtts import gTTS
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
import playsound


def is_online(host="8.8.8.8", port=53, timeout=3):
    """Check for internet connection."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False


def speak_offline(text, lang='fr'):
    """Offline speech using gTTS + pygame."""
    print(f"(🔈 OFFLINE - {lang.upper()}) : {text}")
    try:
        filename = "temp_speech.mp3"
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)

        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        os.remove(filename)

    except Exception as e:
        print(f"[Erreur gTTS] {e}\n[Devait dire : {text}]")


def speak(text, lang='fr', offline=False):
    """
    TTS principal :
    - Si offline=True ou pas de connexion, utilise gTTS.
    - Sinon, utilise ElevenLabs.
    """
    print(f"\n🗣️  {text} ({'OFFLINE' if offline else 'ONLINE'})")

    if not offline and is_online():
        try:
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
                    playsound.playsound("output.mp3")
                    os.remove("output.mp3")
                except Exception as e:
                    print(f"[Erreur lecture audio] {e}")
            else:
                print(f"[Erreur ElevenLabs] {response.text}")
                speak_offline(text, lang)
        except Exception as e:
            print(f"[Exception ElevenLabs] {e}")
            speak_offline(text, lang)
    else:
        if not is_online():
            print("🌐 Pas de connexion. Passage en mode hors ligne.")
        speak_offline(text, lang)

