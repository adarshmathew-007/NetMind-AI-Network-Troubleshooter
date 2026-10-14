import platform
import re
import subprocess


def ping_host(host):
    """
    Ping a host and return structured network diagnostic information.
    """
    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "4", host]
    else:
        command = ["ping", "-c", "4", host]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=15
        )

        output = result.stdout + result.stderr

        if result.returncode == 0:
            status = "reachable"
        else:
            status = "unreachable"

        packet_loss = extract_packet_loss(output)
        latency = extract_latency(output)

        return {
            "host": host,
            "status": status,
            "packet_loss": packet_loss,
            "latency": latency,
            "raw_output": output
        }

    except subprocess.TimeoutExpired:
        return {
            "host": host,
            "status": "timeout",
            "packet_loss": None,
            "latency": None,
            "raw_output": "Ping request timed out."
        }

    except Exception as error:
        return {
            "host": host,
            "status": "error",
            "packet_loss": None,
            "latency": None,
            "raw_output": str(error)
        }


def extract_packet_loss(output):
    """Extract packet loss percentage from ping output."""
    match = re.search(r"\((\d+)% loss\)", output)
    if match:
        return int(match.group(1))
    return None


def extract_latency(output):
    """Extract min, max and average latency from Windows ping output."""
    match = re.search(
        r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms",
        output
    )
    if match:
        return {
            "min_ms": int(match.group(1)),
            "max_ms": int(match.group(2)),
            "average_ms": int(match.group(3))
        }
    return None


if __name__ == "__main__":
    target = input("Enter a host or IP address: ")
    result = ping_host(target)

    print("\n--- NetMind Ping Diagnostic ---")
    print(f"Host: {result['host']}")
    print(f"Status: {result['status']}")
    print(f"Packet Loss: {result['packet_loss']}%")

    if result["latency"]:
        print(f"Minimum Latency: {result['latency']['min_ms']} ms")
        print(f"Maximum Latency: {result['latency']['max_ms']} ms")
        print(f"Average Latency: {result['latency']['average_ms']} ms")

    print("\nRaw Output:")
    print(result["raw_output"])