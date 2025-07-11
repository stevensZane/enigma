# main.py

from listener import listen
from speaker import speak
from commands import is_known_command
from agent import ask_llm

def main():
    while True:
        text = listen()
        if not text:
            continue

        # Check for hardcoded commands
        command_response = is_known_command(text)
        if command_response:
            speak(command_response)
        else:
            llm_response = ask_llm(text)
            speak(llm_response)

if __name__ == "__main__":
    main()
