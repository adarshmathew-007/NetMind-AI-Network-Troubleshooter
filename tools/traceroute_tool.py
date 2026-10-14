import platform
import subprocess


def traceroute_host(host, max_hops=10):
    """Trace the route to a host and return raw output."""
    system = platform.system().lower()

    if system == "windows":
        command = ["tracert", "-h", str(max_hops), host]
    else:
        command = ["traceroute", "-m", str(max_hops), host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=90
        )
        return {
            "host": host,
            "status": "ok",
            "raw_output": result.stdout
        }
    except subprocess.TimeoutExpired:
        return {"host": host, "status": "timeout", "raw_output": ""}
    except Exception as error:
        return {"host": host, "status": "error", "raw_output": str(error)}