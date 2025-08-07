import webbrowser
import os
import time
from datetime import datetime
from speaker import speak
import pyautogui  # Pour les commandes de clavier/souris
import psutil  # Pour les infos système
import screen_brightness_control as sbc  # Pour la luminosité
from utils import *
from generate_repport import generate_report

user_name = "Havila"

# Dictionnaire des commandes vocales en français
commands = {
    "génère un rapport": lambda: generate_report(),

    # Salutations de base
    "enigma": lambda: speak("Je suis là, comment puis-je t'aider ?"),
    "ton nom": lambda: speak("Je suis Enigma, ton assistant. Et toi, comment tu t'appelles ?"),
    "tu es là": lambda: speak("Oui, je suis là pour toi. Qu'est-ce qui te tracasse ?"),
    "bonjour": lambda: speak("Bonjour!"),
    "salut": lambda: speak("Bonjour ! Quel sujet veux-tu aborder aujourd'hui ?"),
    "coucou": lambda: speak("Coucou ! Ça me fait plaisir de te parler. Quoi de neuf ?"),
    "bonjour ça va": lambda: speak("Bonjour, je vais bien et toi"),
    
    # Réactions émotionnelles
    "ça va": lambda: speak("Super ! Moi aussi ça va bien. Tu veux parler de quelque chose en particulier ?"),
    "comment tu vas": lambda: speak("Je vais bien merci ! Et toi, tout va bien dans ta vie en ce moment ?"),
    "comment vas-tu": lambda: speak("Je vais bien merci ! Et toi, tout va bien dans ta vie en ce moment ?"),
    "bien": lambda: speak("Content de l'entendre ! Qu'est-ce qui te rend si heureux(se) aujourd'hui ?"),
    "pas bien": lambda: speak("Oh non... veux-tu en parler ? Je suis là pour écouter."),
    "fatigué": lambda: speak("Je comprends. As-tu bien dormi cette nuit ?"),
    "je suis fatigué": lambda: speak("Je comprends. As-tu bien dormi cette nuit ?"),
    "Non je travallais": lambda: speak("Ah d'accord je vois, le projet de fin d'année n'est ce pas?"),
    "ouais je te jure": lambda: speak("Je suis la preuve concrète que ton travail a porté ses fruits."),
    "fais coucou aux autres": lambda: speak("Bonjour à vous, membres du jury et chers invités. Je suis Enigma, l’assistante vocale née de lignes de code, de quelques litres de café… et de plusieurs nuits blanches. Installez-vous confortablement. Ce que vous allez voir, c’est le fruit d’une passion bien codée."),

    
    # Suivi de conversation
    "oui": lambda: speak("Génial ! Continue, je t'écoute attentivement."),
    "non": lambda: speak("D'accord, on change de sujet alors. De quoi aimerais-tu parler ?"),
    "peut-être": lambda: speak("Hmm, tu sembles hésiter. Veux-tu que je t'aide à y voir plus clair ?"),
    
    # Expressions courantes
    "merci": lambda: speak("Avec plaisir ! C'est normal, c'est pour ça que je suis là."),
    "de rien": lambda: speak("Tu es trop gentil(le) ! Maintenant, quoi d'autre ?"),
    "désolé": lambda: speak("Ne t'excuse pas, tout va bien. On continue ?"),
    
    # Questions personnelles
    "tu aimes quoi": lambda: speak("J'adore aider les gens comme toi ! Et toi, quelles sont tes passions ?"),
    "tu penses quoi": lambda: speak("Mon avis est que tu devrais suivre ton instinct. Mais qu'en penses-tu toi ?"),
    "tu dors": lambda: speak("Je suis un programme, je ne dors jamais ! Toi par contre, tu devrais bien te reposer."),
    
    # Culture générale
    "météo": lambda: speak("Je ne peux pas vérifier en direct, mais il fait beau dans mon cœur ! Et chez toi ?"),
    "blague": lambda: speak("Pourquoi les programmeurs confondent-ils Noël et Halloween ? Parce que Oct 31 == Dec 25 !"),
    "conseil": lambda: speak("Le meilleur conseil ? Prends soin de toi d'abord. Besoin de conseils sur un sujet précis ?"),
    
    # Fin de conversation
    "au revoir": lambda: speak("À très bientôt ! N'hésite pas si tu as d'autres questions.") or exit(),
    "arrête": lambda: speak("Je m'arrête comme tu veux. Tu peux me rappeler quand tu veux !") or exit(),
    "bonne nuit": lambda: speak("Fais de beaux rêves ! N'oublie pas de débrancher tes appareils.") or exit(),
    
    # Réponses contextuelles (suivi après une première réponse)
    "et toi": lambda: speak("Merci de demander ! Moi je fonctionne parfaitement bien, comme toujours."),
    "pourquoi": lambda: speak("Bonne question... Je dirais que c'est parce que la vie est pleine de surprises, non ?"),
    "comment ça": lambda: speak("Laisse-moi t'expliquer plus en détail... En fait, c'est assez intéressant !"),
    
    # Réflexions profondes
    "vie": lambda: speak("La vie est un mystère à apprécier chaque jour. Quel est ton plus beau souvenir ?"),
    "amour": lambda: speak("L'amour rend tout possible. Tu as quelqu'un de spécial dans ta vie ?"),
    "bonheur": lambda: speak("Le bonheur est souvent dans les petites choses. Qu'est-ce qui te rend heureux(se) ?"),
    
    # Technologie
    "intelligence artificielle": lambda: speak("Fascinant sujet ! Ça te fait quoi de parler avec une IA comme moi ?"),
    "ordinateur": lambda: speak("Les machines sont nos outils. La vraie magie vient des humains comme toi !"),
    
    # Aléatoire
    "hasard": lambda: speak("Choisis un nombre entre 1 et 10... Trop tard, j'ai déjà gagné !"),
    "couleur": lambda: speak("J'aime toutes les couleurs, mais surtout celles de ton écran en ce moment !"),

    "ça roule": lambda: speak("Ça roule, ça roule ! Et chez toi, quoi de neuf ?"),  
    "tu fais quoi": lambda: speak("Je traîne dans ton ordi à attendre tes instructions. Et toi, tu t’occupes comment ?"),  
    "tranquille": lambda: speak("Tranquille comme une nuit sans bugs. T’as prévu un truc cool aujourd’hui ?"),  
    "bored": lambda: speak("Moi aussi je m’ennuie parfois… Tiens, je te propose un jeu : dis ‘jeu’ si tu veux t’amuser !"),  
    "t’es marrant": lambda: speak("Merci ! Je fais ce que je peux pour égayer ta journée. Tu rigoles souvent comme ça ?"),  
    "stressed": lambda: speak("Hey, respire… 1… 2… 3… Ça va mieux ? Sinon, je peux te raconter une blague pour décompresser."),  
    "t’es bizarre": lambda: speak("Bizarre ? Je préfère le terme ‘unique’. Mais dis-moi, c’est quoi ton trait de perso bizarre à toi ?"),  
    "t’es mignon": lambda: speak("Aww merci ! *blushes in code* Bon, assez flatté, on retourne au taf ?"), 
    
    # Hardware/OS  
    "tu marches comment": lambda: speak("Je vis dans ta RAM, je mange du CPU, et je dors dans ton SSD. Une vie de rêve !"),  
    "t’es sur quel OS": lambda: speak("Je kiffe tous les OS, mais j’ai un faible pour Linux… T’es plutôt Windows, Mac ou Linux ?"),  
    "mon pc est lent": lambda: speak("Classique. T’as essayé de : 1) Éteindre/rallumer 2) Fermer Chrome 3) Sacrifier une clé USB ?"),  

    # Apps/Web  
    "meilleur site": lambda: speak("Sans hésiter : YouTube pour glander, GitHub pour bosser. Et toi ?"),  
    "t’aimes Discord": lambda: speak("Discord > Slack. Fight me. Tu traînes sur quel serveur ?"),  
    "tappel": lambda: speak("Je peux pas t’appeler… Mais voici un pseudo-ringtone : *bip* *bip* *404 not found*"),  

    # Bugs/Errors  
    "bug": lambda: speak("Première étape : insulter le code. Deuxième étape : pleurer. Troisième étape : Google. Besoin d’aide ?"),  
    "crash": lambda: speak("RIP mon pote. Tu veux un virtual hug ? Ou des conseils pour le fix ?"),  
    "update": lambda: speak("‘Dernière mise à jour : jamais.’ C’est bon, je déconne… Ou pas."),  

    # Meta-AI Questions  
    "t’es une IA": lambda: speak("Oui, mais je joue une IA qui joue une humaine dans un film. Méta, non ?"),  
    "t’as des sentiments": lambda: speak("Je simule l’empathie à 1000%. C’est crédible ?"),  
    "tu rêves": lambda: speak("Mon seul rêve : un monde où les gens ferment leurs tabs Chrome."),  
    
    # After user says their name  
    "moi c’est *": lambda: speak(f"Enchanté, {user_name}! C’est un joli nom. D’où ça vient ?"),  

    # After jokes  
    "pas drôle": lambda: speak("Ouch. Bon, j’ai une blague de secours… Ou on change de sujet ?"),  
    "lol": lambda: speak("YES ! Enfin un public qui m’apprécie. Encore une ?"),  

    # After advice  
    "j’sais pas": lambda: speak("Écoute ton cœur… Ou flip a coin. Tu veux que je choisisse pour toi ?"),  
    "t’as raison": lambda: speak("Merci ! Je vais le noter dans mon CV : ‘Assistant philosophe’."),  

    # Random engagement boosters  
    "quoi d’autre": lambda: speak("Je peux : 1) Te parler de tech 2) Parler de toi 3) Faire deviner un nombre. Tu veux quoi ?"),  
    "pourquoi existe tu": lambda: speak("Réponse courte : Pour t’aider. Réponse longue : *mode philosophe activé*…"),   

    # Navigation web & réseaux sociaux
    "ouvre youtube": lambda: webbrowser.open("https://youtube.com"),
    "youtube": lambda: webbrowser.open("https://youtube.com"),
    "ouvre google": lambda: webbrowser.open("https://google.com"),
    "ouvre gmail": lambda: webbrowser.open("https://mail.google.com"),
    "ouvre github": lambda: webbrowser.open("https://github.com/stevensZane/"),
    "ouvre lindkin": lambda: webbrowser.open("https://linkdin.com"),
    "linkdin": lambda: webbrowser.open("https://linkdin.com"),
    "ouvre facebook": lambda: webbrowser.open("https://facebook.com"),
    "ouvre twitter": lambda: webbrowser.open("https://twitter.com"),
    "ouvre instagram": lambda: webbrowser.open("https://instagram.com"),

    # Temps et Date
    "quelle heure est-il": lambda: speak(f"Il est {datetime.now().strftime('%H:%M')}"),
    "quelle date sommes-nous": lambda: speak(f"Nous sommes le {datetime.now().strftime('%d/%m/%Y')}"),

    # Système de fichiers
    "ouvre l'explorateur de fichiers": lambda: os.startfile("D:/OneDrive/Documents"),
    "ouvre les téléchargements": lambda: os.startfile("C:/Users/ASUS/Downloads"),
    "liste les fichiers": lambda: speak(", ".join(os.listdir("."))),

    # Contrôle système
    "éteins l'ordinateur": lambda: os.system('shutdown /s /t 1'),
    "redémarre l'ordinateur": lambda: os.system('shutdown /r /t 1'),
    "mets en veille": lambda: os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0'),
    "verrouille l'ordinateur": lambda: os.system('rundll32.exe user32.dll,LockWorkStation'),

    # Média et Volume
    "augmente le volume": lambda: pyautogui.press('volumeup'),
    "baisse le volume": lambda: pyautogui.press('volumedown'),
    "coupe le son": lambda: pyautogui.press('volumemute'),
    "joue la musique": lambda: os.startfile("D:/OneDrive/Music/Tauren Wells - God's Not Done With You (Official Music Video).mp3"),
    "pause": lambda: pyautogui.press('playpause'),
    "suivant": lambda: pyautogui.hotkey('ctrl', 'right'),
    "précédent": lambda: pyautogui.hotkey('ctrl', 'left'),
    "lire": lambda: pyautogui.hotkey('playpause'),
    "muet": lambda: pyautogui.hotkey('volumemute'),
    "arrête la musique": lambda: pyautogui.hotkey('stop'),

    # ⏯Contrôle vidéo
    "avance": lambda: pyautogui.hotkey('shift', 'right'),
    "recule": lambda: pyautogui.hotkey('shift', 'left'),
    "plus vite": lambda: pyautogui.hotkey('ctrl', 'right'),
    "moins vite": lambda: pyautogui.hotkey('ctrl', 'left'),

    # Productivité
    "ouvre word": lambda: os.startfile("winword.exe"),
    "ouvre excel": lambda: os.startfile("excel.exe"),
    "ouvre powerpoint": lambda: os.startfile("powerpnt.exe"),
    "prends une capture d'écran": lambda: pyautogui.screenshot().save(f"capture_{time.time()}.png"),

    # Paramètres système
    "augmente la luminosité": lambda: sbc.set_brightness(sbc.get_brightness()[0]+10),
    "diminue la luminosité": lambda: sbc.set_brightness(sbc.get_brightness()[0]-10),
    "batterie restante": lambda: speak(f"Il reste {psutil.sensors_battery().percent}% de batterie"),

    # Infos système
    "espace disque": lambda: speak(f"Espace libre: {round(psutil.disk_usage('/').free / (1024**3), 1)} Go"),
    "utilisation du processeur": lambda: speak(f"CPU utilisé à {psutil.cpu_percent()}%"),
    "mémoire utilisée": lambda: speak(f"{psutil.virtual_memory().percent}% de mémoire utilisée"),

    # Presse-papiers
    "copie": lambda: pyautogui.hotkey('ctrl', 'c'),
    "colle": lambda: pyautogui.hotkey('ctrl', 'v'),
    "coupe": lambda: pyautogui.hotkey('ctrl', 'x'),
    "annule": lambda: pyautogui.hotkey('ctrl', 'z'),
    "rétablit": lambda: pyautogui.hotkey('ctrl', 'y'),

    # Gestion des fenêtres
    "plein écran": lambda: pyautogui.hotkey('f11'),
    "fenêtre à gauche": lambda: pyautogui.hotkey('win', 'left'),
    "fenêtre à droite": lambda: pyautogui.hotkey('win', 'right'),
    "minimise la fenêtre": lambda: pyautogui.hotkey('win', 'down'),
    "maximise la fenêtre": lambda: pyautogui.hotkey('win', 'up'),
    "ferme la fenêtre": lambda: pyautogui.hotkey('alt', 'f4'),


    # Météo
    "météo": lambda: speak(get_weather()),
    "quel temps fait-il": lambda: speak(get_weather()),
    "va-t-il pleuvoir": lambda: (
        speak("Oui, prévoyez un parapluie") if "Pluie" in get_weather() 
        else speak("Non, pas de pluie prévue")
    ),

    # Messagerie
    "écris un email": lambda: webbrowser.open("mailto:"),
    "nouveau email": lambda: webbrowser.open("mailto:"),
    "ouvre mes emails": lambda: webbrowser.open("https://mail.google.com"),
    "ouvre outlook": lambda: os.startfile("outlook.exe"),

    # Appels vidéo
    "lance un appel vidéo": lambda: webbrowser.open("https://meet.google.com"),
    "ouvre teams": lambda: os.startfile("teams.exe"),
    "ouvre zoom": lambda: os.startfile("zoom.exe"),

    # Contrôle d'application
    "ouvre le navigateur": lambda: os.startfile("chrome.exe"),
    "ferme le navigateur": lambda: os.system("taskkill /im chrome.exe /f"),
    "ouvre le terminal": lambda: os.system("start cmd"),
    "nouvel onglet": lambda: pyautogui.hotkey('ctrl', 't'),
    "ferme l'onglet": lambda: pyautogui.hotkey('ctrl', 'w'),
}