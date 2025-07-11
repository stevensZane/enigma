# commands.py

def is_known_command(text):
    text = text.lower()
    if "your name" in text:
        return "My name is Enigma. Nice to meet you!"
    if "hello" in text or "hi" in text:
        return "Hello! How can I help you?"
    return None

import subprocess
import os
import webbrowser
import datetime
import time
import random
from typing import Dict, Union

def parse_user_command(text: str) -> Dict[str, Union[str, None]]:
    """
    Analyse la commande vocale et retourne un dictionnaire structuré.
    Si aucune commande spécifique n'est reconnue, retourne une commande pour le LLM généraliste.
    """
    text = text.lower()
    
    # A. Commandes Générales et d'Interaction
    if any(greeting in text for greeting in ["salut", "bonjour", "hello", "hi"]):
        return {"action": "greet", "response_text": "Bonjour ! Comment puis-je vous aider ?"}
    
    if "comment tu vas" in text:
        return {"action": "status", "response_text": "Je fonctionne parfaitement, merci !"}
    
    if "quelle heure est-il" in text:
        return {"action": "tell_time", "response_text": None}
    
    if "quelle est la date" in text:
        return {"action": "tell_date", "response_text": None}
    
    if "blague" in text:
        return {"action": "tell_joke", "response_text": None}
    
    if any(cmd in text for cmd in ["arrête d'écouter", "mets-toi en veille"]):
        return {"action": "sleep", "response_text": "Je passe en mode veille. Dites 'Bonjour Vical' pour me réactiver."}

    # B. Navigation Système
    if "ouvre l'explorateur" in text:
        return {"action": "open_file_explorer", "response_text": "Ouverture de l'Explorateur de fichiers."}
    
    if "va sur mon bureau" in text:
        return {"action": "open_folder", "folder": "desktop", "response_text": "Ouverture du Bureau."}
    
    if "ouvre le dossier documents" in text:
        return {"action": "open_folder", "folder": "documents", "response_text": "Ouverture des Documents."}
    
    if "recherche" in text and "dans" in text:
        parts = text.split("dans")
        search_term = parts[0].replace("recherche", "").strip()
        folder = parts[1].strip()
        return {"action": "search_file", "search_term": search_term, "folder": folder, "response_text": f"Recherche de '{search_term}' dans {folder}."}
    
    if "ouvre les paramètres" in text:
        return {"action": "open_settings", "response_text": "Ouverture des Paramètres Windows."}

    # C. Gestion Applications
    if "lance" in text or "ouvre" in text:
        app_name = text.replace("lance", "").replace("ouvre", "").strip()
        if app_name:
            return {"action": "open_app", "app_name": app_name, "response_text": f"Ouverture de {app_name}."}
    
    if "ferme" in text:
        app_name = text.replace("ferme", "").strip()
        if app_name:
            return {"action": "close_app", "app_name": app_name, "response_text": f"Fermeture de {app_name}."}
    
    if "minimise toutes les fenêtres" in text:
        return {"action": "minimize_all", "response_text": "Minimisation de toutes les fenêtres."}
    
    if "gestionnaire des tâches" in text:
        return {"action": "open_task_manager", "response_text": "Ouverture du Gestionnaire des tâches."}

    # D. Web et Recherche
    if "ouvre google" in text:
        return {"action": "open_website", "url": "https://google.com", "response_text": "Ouverture de Google."}
    
    if "recherche" in text and "sur internet" in text:
        query = text.replace("recherche", "").replace("sur internet", "").strip()
        return {"action": "web_search", "query": query, "response_text": f"Recherche de '{query}' sur internet."}
    
    if "météo à" in text:
        city = text.replace("météo à", "").strip()
        return {"action": "weather", "city": city, "response_text": f"Obtention de la météo pour {city}."}

    # E. Multimédia
    if "mets de la musique" in text:
        return {"action": "play_music", "response_text": "Lancement de la musique."}
    
    if any(cmd in text for cmd in ["monte le volume", "augmente le volume"]):
        return {"action": "volume_up", "response_text": "Volume augmenté."}
    
    if any(cmd in text for cmd in ["baisse le volume", "réduis le volume"]):
        return {"action": "volume_down", "response_text": "Volume baissé."}
    
    if any(cmd in text for cmd in ["mute le son", "désactive le son"]):
        return {"action": "volume_mute", "response_text": "Son désactivé."}

    # F. Utilitaires
    if "éteins l'ordinateur" in text:
        return {"action": "shutdown", "response_text": "Extinction de l'ordinateur dans 30 secondes."}
    
    if "redémarre l'ordinateur" in text:
        return {"action": "restart", "response_text": "Redémarrage de l'ordinateur dans 30 secondes."}
    
    if "verrouille mon écran" in text:
        return {"action": "lock_screen", "response_text": "Verrouillage de l'écran."}

    # Si aucune commande reconnue
    return {"action": "llm_query", "response_text": None}

def execute_command(command_data: Dict) -> str:
    """Exécute la commande système correspondante et retourne un message de statut"""
    try:
        action = command_data["action"]
        
        # A. Commandes Générales
        if action == "greet":
            return command_data["response_text"]
            
        elif action == "tell_time":
            return f"Il est {datetime.datetime.now().strftime('%H:%M')}"
            
        elif action == "tell_date":
            return f"Nous sommes le {datetime.datetime.now().strftime('%d/%m/%Y')}"
            
        elif action == "tell_joke":
            jokes = ["Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau !",
                    "Quel est le comble pour un électricien ? De ne pas être au courant !"]
            return random.choice(jokes)
        
        # B. Navigation Système
        elif action == "open_file_explorer":
            subprocess.Popen("explorer")
            return command_data["response_text"]
            
        elif action == "open_folder":
            folder = command_data["folder"]
            if folder == "desktop":
                os.startfile(os.path.join(os.path.expanduser("~"), "Desktop"))
            elif folder == "documents":
                os.startfile(os.path.join(os.path.expanduser("~"), "Documents"))
            return command_data["response_text"]
        
        # C. Gestion Applications
        elif action == "open_app":
            app_name = command_data["app_name"]
            if "chrome" in app_name:
                subprocess.Popen("start chrome", shell=True)
            elif "word" in app_name:
                subprocess.Popen("start winword", shell=True)
            else:
                os.startfile(app_name)
            return command_data["response_text"]
            
        elif action == "minimize_all":
            subprocess.Popen("powershell (New-Object -ComObject Shell.Application).MinimizeAll()", shell=True)
            return command_data["response_text"]
        
        # D. Web et Recherche
        elif action == "open_website":
            webbrowser.open(command_data["url"])
            return command_data["response_text"]
            
        elif action == "web_search":
            webbrowser.open(f"https://www.google.com/search?q={command_data['query']}")
            return command_data["response_text"]
        
        # E. Multimédia
        elif action == "play_music":
            music_dir = os.path.join(os.path.expanduser("~"), "Music")
            os.startfile(music_dir)
            return command_data["response_text"]
        
        # F. Utilitaires
        elif action == "shutdown":
            subprocess.Popen("shutdown /s /t 30", shell=True)
            return command_data["response_text"]
            
        elif action == "lock_screen":
            subprocess.Popen("rundll32.exe user32.dll,LockWorkStation")
            return command_data["response_text"]
        
        else:
            return "Commande non implémentée"
            
    except Exception as e:
        return f"Erreur lors de l'exécution: {str(e)}"

def is_known_command(text: str) -> Union[str, None]:
    """Vérifie si le texte correspond à une commande connue (version simplifiée)"""
    result = parse_user_command(text)
    if result["action"] != "llm_query":
        return result["response_text"] or "Commande exécutée"
    return None