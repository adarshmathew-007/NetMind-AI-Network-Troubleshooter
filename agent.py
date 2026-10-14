import json
from tools.ping_tool import ping_host
from tools.dns_tool import dns_lookup
from tools.traceroute_tool import traceroute_host


TOOLS = {
    "ping": {
        "fn": ping_host,
        "desc": "Check if a host is reachable. Args: host (string)"
    },
    "dns_lookup": {
        "fn": dns_lookup,
        "desc": "Resolve a domain to an IP. Args: domain (string)"
    },
    "traceroute": {
        "fn": traceroute_host,
        "desc": "Trace the route to a host. Args: host (string)"
    }
}

SYSTEM_PROMPT = """
You are NetMind, a network troubleshooting AI agent.
Investigate network problems by calling diagnostic tools one at a time.

Available tools:
- ping(host)          : check reachability
- dns_lookup(domain)  : check DNS resolution
- traceroute(host)    : find where packets stop

Reply ONLY with valid JSON in one of these two forms.

To call a tool:
{"action": "tool", "tool": "ping", "args": {"host": "8.8.8.8"}, "reason": "why you chose this"}

To finish with the final diagnosis:
{"action": "final", "root_cause": "...", "evidence": "...", "fix_steps": ["step 1", "step 2"]}

Rules:
- Call one tool at a time.
- Look at each tool result before deciding the next tool.
- Do not repeat the same tool with the same argument.
- Stop as soon as you have enough evidence.
"""


def run_agent(problem, call_llm, max_steps=5):
    try:
        history = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Problem: {problem}"}
        ]
        trace = []

        for step in range(max_steps):
            reply = call_llm(history)
            history.append({"role": "assistant", "content": reply})

            clean = reply.strip().replace("```json", "").replace("```", "").strip()

            try:
                decision = json.loads(clean)
            except json.JSONDecodeError:
                raise ValueError("LLM did not return valid JSON")

            if decision.get("action") == "final":
                decision["trace"] = trace
                decision["mode"] = "gemini"
                return decision

            tool_name = decision.get("tool")
            args = decision.get("args", {})
            tool = TOOLS.get(tool_name)

            if not tool:
                history.append({
                    "role": "user",
                    "content": f"Tool {tool_name} does not exist. Use only {list(TOOLS)}."
                })
                continue

            result = tool["fn"](**args)

            trace.append({
                "step": step + 1,
                "tool": tool_name,
                "args": args,
                "reason": decision.get("reason", ""),
                "result": result
            })

            history.append({
                "role": "user",
                "content": f"Tool {tool_name} returned: {json.dumps(result)}"
            })

        raise ValueError("Max steps reached")

    except Exception as error:
        print(f"[NetMind] Gemini unavailable ({error}). Switching to offline engine.")
        from offline_agent import run_offline_agent
        return run_offline_agent(problem)