from agent import run_agent
from llm import call_llm


problem = "I can't open any websites, but the Wi-Fi icon shows connected."

result = run_agent(problem, call_llm)

print("\n===== FINAL RESULT =====")
print(result)

print("\n===== INVESTIGATION TRACE =====")
for entry in result.get("trace", []):
    print(entry)