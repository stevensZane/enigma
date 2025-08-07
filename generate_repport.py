# report_generator.py
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def generate_report(csv_path="interactions.csv", output_path="rapport_test_utilisateur.pdf"):
    df = pd.read_csv(csv_path)

    # Nettoyage de base
    df["Date_Test"] = pd.to_datetime(df["Date_Test"])
    df["Tps_Execution_Sec"] = pd.to_numeric(df["Tps_Execution_Sec"], errors="coerce")
    df["Difficulte_Score_1_5"] = pd.to_numeric(df["Difficulte_Score_1_5"], errors="coerce")

    # Analyses simples
    total_commandes = len(df)
    taux_succès = round(df["Tache_Accomplie"].str.upper().eq("VRAI").mean() * 100, 2)
    duree_moy = round(df["Tps_Execution_Sec"].mean(), 2)
    difficulte_moy = round(df["Difficulte_Score_1_5"].mean(), 2)

    # Création du PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Rapport d'évaluation de l'assistant vocal", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt=f"Nombre total de commandes testées : {total_commandes}", ln=True)
    pdf.cell(200, 10, txt=f"Taux de réussite : {taux_succès}%", ln=True)
    pdf.cell(200, 10, txt=f"Temps moyen d'exécution : {duree_moy} secondes", ln=True)
    pdf.cell(200, 10, txt=f"Score moyen de difficulté : {difficulte_moy}/5", ln=True)

    # Ajout de graphes
    try:
        df["Tache_Accomplie"].value_counts().plot(kind='bar', color=["green", "red"])
        plt.title("Tâches accomplies vs échouées")
        plt.xlabel("Tâche accomplie")
        plt.ylabel("Nombre")
        plt.tight_layout()
        plt.savefig("graph1.png")
        plt.close()

        pdf.add_page()
        pdf.image("graph1.png", x=10, y=30, w=180)
        os.remove("graph1.png")
    except:
        pass

    pdf.output(output_path)
    print(f"✅ Rapport généré : {output_path}")
    return output_path
