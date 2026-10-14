import socket


def dns_lookup(domain):
    """Resolve a domain name and return structured result."""
    try:
        ip = socket.gethostbyname(domain)
        return {
            "domain": domain,
            "status": "resolved",
            "ip": ip
        }
    except socket.gaierror as error:
        return {
            "domain": domain,
            "status": "failed",
            "error": str(error)
        }
    except Exception as error:
        return {
            "domain": domain,
            "status": "error",
            "error": str(error)
        }


if __name__ == "__main__":
    target = input("Enter a domain: ")
    print(dns_lookup(target))