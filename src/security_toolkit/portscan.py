"""TCP connect port scanner with optional banner grabbing."""
from __future__ import annotations

import socket
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional, Sequence

from .core import banner_grab, service_for


def scan_one(
    host: str,
    port: int,
    timeout: float = 1.0,
    grab_banner: bool = False,
) -> dict:
    result: dict = {"port": port, "open": False, "service": None, "banner": None}
    try:
        with socket.create_connection((host, port), timeout=timeout):
            result["open"] = True
            result["service"] = service_for(port)
            if grab_banner:
                result["banner"] = banner_grab(host, port, timeout=timeout)
    except OSError:
        pass
    return result


def scan(
    host: str,
    ports: Sequence[int],
    timeout: float = 1.0,
    max_threads: int = 128,
    grab_banner: bool = False,
) -> List[dict]:
    """Scan `host` across `ports`. Returns results for OPEN ports only."""
    results: List[dict] = []
    with ThreadPoolExecutor(max_workers=max_threads) as pool:
        futures = [pool.submit(scan_one, host, p, timeout, grab_banner) for p in ports]
        for fut in futures:
            r = fut.result()
            if r["open"]:
                results.append(r)
    results.sort(key=lambda r: r["port"])
    return results
