# import requests
# import time
# from config import OPENROUTER_API_KEY

# def ask_llm(prompt, retries=3):
#     url = "https://openrouter.ai/api/v1/chat/completions"

#     headers = {
#         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": "https://myvoiceagent.local"
#     }
#     payload = {
#         "model": "mistralai/mistral-7b-instruct",  # More stable
#         "messages": [{"role": "user", "content": prompt}]
#     }

#     for attempt in range(retries):
#         try:
#             response = requests.post(url, headers=headers, json=payload, timeout=20)
#             response.raise_for_status()
#             data = response.json()
#             return data["choices"][0]["message"]["content"].strip()
#         except requests.exceptions.RequestException as e:
#             print(f"❌ Attempt {attempt+1}/{retries} failed: {e}")
#             time.sleep(1.5)  # Wait a bit before retrying

#     return "Sorry, I had trouble thinking that through."

import requests
import time
import json

def ask_llm(prompt, retries=3):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "deepseek-llm:7b-chat",
        "prompt": prompt,
        "stream": True
    }

    for attempt in range(retries):
        try:
            start = time.time()
            response = requests.post(url, json=payload, stream=True, timeout=60)
            response.raise_for_status()

            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))  # ✅ JSON-safe
                        chunk = data.get("response", "")
                        print(chunk, end="", flush=True)
                        full_response += chunk
                    except Exception as e:
                        print(f"\n[stream error] {e}")
                        break

            end = time.time()
            print(f"\n⏱️ Responded in {end - start:.2f} seconds")
            return full_response.strip()

        except requests.exceptions.RequestException as e:
            print(f"❌ Attempt {attempt+1}/{retries} failed: {e}")
            time.sleep(1.5)

    return "Sorry, I had trouble thinking that through."


