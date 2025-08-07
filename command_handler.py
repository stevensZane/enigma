# command_handler.py
from commands import commands
import webbrowser
import random

def get_polite_fallback():
    """Returns random polite phrases for unrecognized commands"""
    phrases = [
        "Désolé, je ne reconnais pas cette commande. Vous pouvez consulter les commandes disponibles.",
        "Je ne suis pas sûr de comprendre. Voici quelques exemples de commandes que vous pouvez essayer.",
        "Cette instruction ne fait pas partie de mes compétences actuelles. Essayez une commande connue.",
        "Je n'ai pas compris. Pour voir ce que je peux faire, dites par exemple : 'liste des commandes'.",
        "Cette commande n’est pas disponible. Besoin d’aide ? Dites : 'quelles sont les commandes disponibles'.",
        "Hmm... cela ne me dit rien. Vous pouvez demander 'aide' pour voir mes commandes.",
        "Je ne suis pas programmé pour cela. Consultez les commandes prises en charge pour continuer.",
        "Commande inconnue. Pour voir les instructions disponibles, dites simplement 'aide'."
    ]
    return random.choice(phrases)

def handle_command(texte):
    """
    Gère et exécute une commande reconnue ou une recherche dynamique.

    Retourne :
        Tuple : (booléen succès, str réponse)
    """
    texte = texte.lower().strip()

    # Commandes de recherche dynamique
    commandes_recherche = {
        "recherche sur youtube": lambda query: f"https://youtube.com/results?search_query={query}",
        "recherche sur wikipedia": lambda query: f"https://fr.wikipedia.org/wiki/{query.replace(' ', '_')}",
        "recherche": lambda query: f"https://google.com/search?q={query}",
        "cherche": lambda query: f"https://google.com/search?q={query}",
        "trouve": lambda query: f"https://google.com/search?q={query}",
        "google": lambda query: f"https://google.com/search?q={query}",
    }

    for cmd in commandes_recherche:
        if cmd in texte:
            requete = texte.replace(cmd, "").strip()
            if not requete:
                return (False, "Quelle recherche souhaitez-vous effectuer ?")
            url = commandes_recherche[cmd](requete)
            webbrowser.open(url)
            print(f"🔎 Recherche effectuée : {requete}")
            return (True, f"Recherche lancée pour : {requete}")

    # Commandes prédéfinies (fixes)
    if texte in commands:
        print(f"Commande reconnue : {texte}")
        try:
            commands[texte]()  # Exécuter la fonction associée
            return (True, "")
        except Exception as e:
            erreur = f"Erreur d'exécution : {str(e)}"
            print(f"Erreur lors de l'exécution de '{texte}' : {e}")
            return (False, erreur)

    # Si aucune commande trouvée
    reponse_polie = get_polite_fallback()
    print(f"Commande inconnue : {texte} → {reponse_polie}")
    return (False, reponse_polie)
