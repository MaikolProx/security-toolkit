"""Directory brute-forcing: probe a wordlist against a base URL."""
from __future__ import annotations

import http.client
import ssl
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable, List
from urllib.parse import urlparse


def probe(base_url: str, path: str, timeout: float = 5.0) -> int:
    """Return the HTTP status code for GET base_url/path."""
    parsed = urlparse(base_url.rstrip("/"))
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    ctx = ssl.create_default_context() if parsed.scheme == "https" else None
    conn_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    try:
        conn = conn_cls(host, port, timeout=timeout, context=ctx)
        conn.request("GET", f"/{path}", headers={"User-Agent": "sec-tool/dirbust"})
        resp = conn.getresponse()
        status = resp.status
        conn.close()
        return status
    except Exception:  # noqa: BLE001
        return 0


def bust(
    base_url: str,
    wordlist: Iterable[str],
    statuses: Iterable[int] = (200, 204, 301, 302, 403),
    max_threads: int = 32,
    timeout: float = 5.0,
) -> List[tuple[str, int]]:
    """Return [(path, status)] for paths whose status is in `statuses`."""
    hits: List[tuple[str, int]] = []
    with ThreadPoolExecutor(max_workers=max_threads) as pool:
        futures = []
        for word in wordlist:
            word = word.strip().strip("/")
            if not word:
                continue
            futures.append((word, pool.submit(probe, base_url, word, timeout)))
        for word, fut in futures:
            status = fut.result()
            if status in statuses:
                hits.append((word, status))
    hits.sort()
    return hits
