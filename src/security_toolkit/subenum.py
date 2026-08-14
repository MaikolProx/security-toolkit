"""Subdomain enumeration via DNS lookups against a wordlist."""
from __future__ import annotations

import socket
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable, List


def resolve(name: str, timeout: float = 2.0) -> bool:
    """Return True if the hostname resolves (A record exists)."""
    try:
        socket.getaddrinfo(name, None)
        return True
    except socket.gaierror:
        return False


def enumerate_subdomains(
    domain: str,
    wordlist: Iterable[str],
    max_threads: int = 64,
    timeout: float = 2.0,
) -> List[str]:
    """Return the list of subdomains that resolve.

    The wordlist entries are used verbatim (strip whitespace); the domain is
    appended as <word>.<domain>.
    """
    found: List[str] = []
    with ThreadPoolExecutor(max_workers=max_threads) as pool:
        futures = []
        for word in wordlist:
            word = word.strip()
            if not word:
                continue
            fqdn = f"{word}.{domain}"
            futures.append((fqdn, pool.submit(resolve, fqdn, timeout)))
        for fqdn, fut in futures:
            if fut.result():
                found.append(fqdn)
    return sorted(found)


def read_wordlist(path: str) -> List[str]:
    return [line.strip() for line in Path(path).read_text(encoding="utf-8", errors="replace").splitlines() if line.strip()]
