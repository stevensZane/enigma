# logger.py
import csv
import os
import uuid
from datetime import datetime
from utils import command_difficulty
import pandas as pd

CSV_FILE = "interaction_logs.csv"

FIELDNAMES = [
    "ID_Testeur",
    "Date_Test",
    "Scénario_ID",
    "Commande_Proferée",
    "Transcription_ASR",
    "Reponse_Assistant",
    "Tache_Accomplie",
    "Tps_Execution_Sec",
    "Difficulte_Score_1_5",
    "Notes_Observateur",
    "Feedback_Qualitatif_Testeur"
]

# Génère un ID_Testeur et Scénario_ID uniques à la session
ID_Testeur = "T_" + uuid.uuid4().hex[:8].upper()
Scénario_ID = "S_" + datetime.now().strftime("%Y%m%d_%H%M%S")

def get_session_ids():
    return ID_Testeur, Scénario_ID

def log_interaction(id_testeur, date_test, scenario_id, commande, tache_accomplie, tps_execution, sortie_assistant):
    difficulte = command_difficulty.get(commande.lower(), None)  # retourne None si non défini
    ligne = {
        "ID_Testeur": id_testeur,
        "Date_Test": date_test,
        "Scénario_ID": scenario_id,
        "Commande_Proferée": commande,
        "Tache_Accomplie": tache_accomplie,
        "Tps_Execution_Sec": tps_execution,
        "Reponse_Assistant": sortie_assistant,
        "Difficulte_Score_1_5": difficulte
    }
    df = pd.DataFrame([ligne])
    df.to_csv("interactions.csv", mode="a", header=not os.path.exists("interactions.csv"), index=False)
