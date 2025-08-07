
import speech_recognition as sr

def listen(preferred_language='fr-FR'):
    """
    Écoute de la parole en français et retourne le texte transcrit.
    
    Paramètres :
        preferred_language (str) : Langue à utiliser (par défaut : 'fr-FR')
    
    Retourne :
        str : Le texte transcrit en minuscules
    """
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    # Configuration
    recognizer.pause_threshold = 0.6
    recognizer.energy_threshold = 150
    recognizer.dynamic_energy_threshold = True
    phrase_time_limit = 8


    print("Calibration du micro (bruit ambiant)...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)

    print("Parlez en français... (pause pour arrêter)")

    final_text = ""
    is_listening = True

    while is_listening:
        try:
            with mic as source:
                print("En écoute...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)

            try:
                text = recognizer.recognize_google(audio, language=preferred_language)
                print(f"Vous avez dit : {text}")
                final_text += " " + text
            except sr.UnknownValueError:
                print("Parole non reconnue ou silence détecté.")
                is_listening = False
            except sr.RequestError as e:
                print(f"Erreur du service de reconnaissance : {e}")
                is_listening = False

        except sr.WaitTimeoutError:
            print("Temps d'attente écoulé, arrêt de l'écoute.")
            is_listening = False

    final_result = final_text.strip().lower()
    print("\nTranscription finale :")
    print(final_result)
    return final_result
