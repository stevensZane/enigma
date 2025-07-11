import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Configuration
    recognizer.pause_threshold = 1.0  # Time to wait after user stops talking
    recognizer.energy_threshold = 300  # Minimum audio energy to consider as speech
    recognizer.dynamic_energy_threshold = True  # Helps with varying mic sensitivity

    print("🔊 Adjusting for ambient noise...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)

    print("🎤 Start speaking (wait for silence to stop)...")
    
    final_text = ""
    is_listening = True
    
    while is_listening:
        try:
            with mic as source:
                print("👂 Listening...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"🗣️ You said: {text}")
                    final_text += " " + text
                except sr.UnknownValueError:
                    print("🔇 Silence detected, stopping...")
                    is_listening = False
                except sr.RequestError as e:
                    print(f"🚫 API error: {e}")
                    is_listening = False
                    
        except sr.WaitTimeoutError:
            print("⏳ No speech detected within timeout period, stopping...")
            is_listening = False
    
    print("\n🎤 Final transcript:")
    print(final_text.strip().lower())
    return final_text.strip().lower()