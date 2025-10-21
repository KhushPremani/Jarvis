import asyncio
import socket
from typing import Dict

# small safe default port list — change only for VMs/labs you own
COMMON_PORTS = [22, 80, 443, 3306, 8080]

async def _check_port(host: str, port: int, timeout: float = 1.0) -> Dict:
    loop = asyncio.get_event_loop()
    try:
        fut = loop.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        await asyncio.wait_for(fut, timeout=timeout)
        # attempt connect
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.settimeout(timeout)
        try:
            conn.connect((host, port))
            conn.close()
            return {"port": port, "open": True}
        except Exception:
            return {"port": port, "open": False}
    except Exception:
        return {"port": port, "open": False}

async def scan_ports(host: str, ports: list = COMMON_PORTS) -> list:
    """Async scan of a small list of ports. Safe: keep default list small."""
    tasks = [_check_port(host, p) for p in ports]
    results = await asyncio.gather(*tasks)
    return results

# quick local test
if __name__ == "__main__":
    import asyncio
    print(asyncio.run(scan_ports("127.0.0.1")))
  
