import time
from listener import listen
from speaker import speak
from command_handler import handle_command
from logger import log_interaction, get_session_ids
from datetime import datetime

def main():
    speak("Salut, je suis Enigma. Je suis là pour vous aider.", lang='fr', offline=True)
    ID_Testeur, Scénario_ID = get_session_ids()
    print(f"Session : {ID_Testeur} / {Scénario_ID}")

    while True:
        
        texte = listen()
        if not texte:
            continue
        

        start = time.time()
        success, response = handle_command(texte)
        duration = time.time() - start

        # if not response:
        #     response = "Commande exécutée."

        speak(response, lang='fr', offline=True)

        # Logging automatique
        log_interaction(
            id_testeur=ID_Testeur,
            date_test=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            scenario_id=Scénario_ID,
            commande=texte,
            tache_accomplie=success,
            tps_execution=duration,
            sortie_assistant=response
        )

if __name__ == "__main__":
    main()