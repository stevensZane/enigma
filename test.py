from agent import ask_llm
import time

start = time.time()
response = ask_llm("square root of 16")
end = time.time()

print(response)
print(f"⏱️ Responded in {end - start:.2f} seconds")
