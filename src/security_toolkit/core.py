"""Shared helpers: port-range parsing and common service classification."""
from __future__ import annotations

import socket
from typing import List, Optional

COMMON_PORTS: dict[int, str] = {
    21: "ftp", 22: "ssh", 23: "telnet", 25: "smtp", 53: "dns", 80: "http",
    110: "pop3", 135: "msrpc", 139: "netbios-ssn", 143: "imap", 443: "https",
    445: "microsoft-ds", 993: "imaps", 995: "pop3s", 1433: "mssql", 1521: "oracle",
    2049: "nfs", 3306: "mysql", 3389: "rdp", 5432: "postgresql", 5900: "vnc",
    5985: "winrm-http", 5986: "winrm-https", 6379: "redis", 8080: "http-proxy",
    8443: "https-alt", 8888: "http-alt", 9200: "elasticsearch", 27017: "mongodb",
}


def parse_ports(spec: str) -> List[int]:
    """Parse a port spec like '22', '22,80,443', '1-1000' or a mix.

    Raises ValueError for out-of-range ports.
    """
    ports: List[int] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            if not (1 <= start <= 65535 and 1 <= end <= 65535) or start > end:
                raise ValueError(f"rango de puertos inválido: {part}")
            ports.extend(range(start, end + 1))
        else:
            p = int(part)
            if not 1 <= p <= 65535:
                raise ValueError(f"puerto fuera de rango: {part}")
            ports.append(p)
    return sorted(set(ports))


def service_for(port: int) -> Optional[str]:
    """Return the service name for a well-known port, else None."""
    return COMMON_PORTS.get(port)


def banner_grab(host: str, port: int, timeout: float = 3.0) -> Optional[str]:
    """Connect and read up to 512 bytes of banner text (best effort)."""
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            data = sock.recv(512)
            return data.decode(errors="replace").strip() or None
    except OSError:
        return None
