import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import webbrowser

load_dotenv()

def get_weather(location="Paris"):
    """Récupère la météo avec alertes automatiques"""
    API_KEY = os.getenv("OWM_API_KEY")
    if not API_KEY:
        return "Configurez votre clé API OpenWeatherMap dans le fichier .env"

    try:
        # Requête API
        url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric&lang=fr&cnt=5"
        data = requests.get(url).json()
        
        # Données actuelles
        current = data['list'][0]
        temp = current['main']['temp']
        desc = current['weather'][0]['description']
        
        # Détection des alertes
        alerts = []
        for forecast in data['list']:
            time = datetime.fromtimestamp(forecast['dt']).strftime('%H:%M')
            weather_id = forecast['weather'][0]['id']
            
            if 500 <= weather_id < 600:  # Pluie
                alerts.append(f"Pluie prévue à {time}")
            elif 200 <= weather_id < 300:  # Orage
                alerts.append(f"Orage à {time}")
            elif 600 <= weather_id < 700:  # Neige
                alerts.append(f"Neige à {time}")

        # Construction du message
        message = f"Météo à {location}: {temp}°C, {desc}."
        if alerts:
            message += f" ALERTE: {' '.join(alerts)}"
        
        return message

    except Exception as e:
        return f"Erreur météo: {str(e)}"


def handle_search(texte):
    search_commands = {
        "recherche sur youtube": lambda query: f"https://youtube.com/results?search_query={query}",
        "recherche sur wikipedia": lambda query: f"https://fr.wikipedia.org/wiki/{query.replace(' ', '_')}",
        "recherche": lambda query: f"https://google.com/search?q={query}",
        "cherche": lambda query: f"https://google.com/search?q={query}",
        "trouve": lambda query: f"https://google.com/search?q={query}",
        "google": lambda query: f"https://google.com/search?q={query}",
    }

    for cmd in search_commands:
        if cmd in texte:
            query = texte.replace(cmd, "").strip()
            url = search_commands[cmd](query)
            webbrowser.open(url)
            return True  # handled
    return False  # not handled


command_difficulty = {
    "génère un rapport": 4,
    
    "enigma": 1,
    "ton nom": 1,
    "tu es là": 1,
    "bonjour": 1,
    "salut": 1,
    "coucou": 1,
    "merci": 1,
    "au revoir": 1,
    "arrête": 1,

    "ouvre youtube": 1,
    "youtube": 1,
    "ouvre google": 1,
    "ouvre gmail": 1,
    "ouvre github": 1,
    "ouvre lindkin": 1,
    "linkdin": 1,
    "ouvre facebook": 1,
    "ouvre twitter": 1,
    "ouvre instagram": 1,

    "quelle heure est-il": 1,
    "quelle date sommes-nous": 1,

    "ouvre l'explorateur de fichiers": 2,
    "ouvre les téléchargements": 2,
    "liste les fichiers": 3,

    "éteins l'ordinateur": 2,
    "redémarre l'ordinateur": 2,
    "mets en veille": 2,
    "verrouille l'ordinateur": 2,

    "augmente le volume": 1,
    "baisse le volume": 1,
    "coupe le son": 1,
    "joue la musique": 2,
    "pause": 1,
    "suivant": 1,
    "précédent": 1,
    "lire": 1,
    "muet": 1,
    "arrête la musique": 1,

    "avance": 2,
    "recule": 2,
    "plus vite": 2,
    "moins vite": 2,

    "ouvre word": 2,
    "ouvre excel": 2,
    "ouvre powerpoint": 2,
    "prends une capture d'écran": 3,

    "augmente la luminosité": 3,
    "diminue la luminosité": 3,
    "batterie restante": 3,

    "espace disque": 3,
    "utilisation du processeur": 3,
    "mémoire utilisée": 3,

    "copie": 1,
    "colle": 1,
    "coupe": 1,
    "annule": 1,
    "rétablit": 1,

    "plein écran": 1,
    "fenêtre à gauche": 2,
    "fenêtre à droite": 2,
    "minimise la fenêtre": 1,
    "maximise la fenêtre": 1,

    "météo": 4,
    "quel temps fait-il": 4,
    "va-t-il pleuvoir": 4,

    "écris un email": 2,
    "nouveau email": 2,
    "ouvre mes emails": 1,
    "ouvre outlook": 2,

    "lance un appel vidéo": 2,
    "ouvre teams": 2,
    "ouvre zoom": 2,

    "ouvre le navigateur": 1,
    "ferme le navigateur": 2,
    "ouvre le terminal": 2,
    "nouvel onglet": 1,
    "ferme l'onglet": 1
  }