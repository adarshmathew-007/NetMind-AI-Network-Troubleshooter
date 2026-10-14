from tools.ping_tool import ping_host
from tools.dns_tool import dns_lookup


def run_offline_agent(problem):
    """
    Offline rule-based network troubleshooting engine.
    Diagnoses connectivity problems without using an LLM.
    """
    trace = []

    # Step 1: ping 8.8.8.8
    ping_result = ping_host("8.8.8.8")
    trace.append({
        "step": 1,
        "tool": "ping",
        "args": {"host": "8.8.8.8"},
        "reason": "Check external IP reachability to primary DNS server (8.8.8.8)",
        "result": ping_result,
    })

    if ping_result.get("status") != "reachable":
        return {
            "action": "final",
            "root_cause": "No external internet connectivity",
            "evidence": f"Ping to 8.8.8.8 failed with status '{ping_result.get('status')}'.",
            "fix_steps": [
                "Check Wi-Fi/Ethernet connection",
                "Restart the router",
                "Check WAN cable",
                "Contact ISP if it continues",
            ],
            "trace": trace,
            "mode": "offline-rule-engine",
        }

    # Step 2: if ping OK, call dns_lookup("google.com")
    dns_result = dns_lookup("google.com")
    trace.append({
        "step": 2,
        "tool": "dns_lookup",
        "args": {"domain": "google.com"},
        "reason": "Check DNS resolution for google.com",
        "result": dns_result,
    })

    if dns_result.get("status") != "resolved":
        return {
            "action": "final",
            "root_cause": "DNS resolution failure",
            "evidence": f"DNS resolution for google.com failed: {dns_result.get('error', 'Unable to resolve')}.",
            "fix_steps": [
                "Set DNS to 1.1.1.1 and 8.8.8.8",
                "Run: ipconfig /flushdns",
                "Retry the website",
            ],
            "trace": trace,
            "mode": "offline-rule-engine",
        }

    # If everything passes
    return {
        "action": "final",
        "root_cause": "No obvious network fault detected",
        "evidence": f"Ping to 8.8.8.8 succeeded and DNS lookup for google.com resolved to {dns_result.get('ip')}.",
        "fix_steps": [
            "Try the specific website again",
            "Clear browser cache",
            "The issue may be server-side",
        ],
        "trace": trace,
        "mode": "offline-rule-engine",
    }
