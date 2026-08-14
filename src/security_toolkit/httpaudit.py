"""HTTP security header audit."""
from __future__ import annotations

import http.client
import ssl
from dataclasses import dataclass, field
from typing import Dict, List
from urllib.parse import urlparse

# (cabecera, descripción) — solo las de mayor impacto
CHECKLIST: Dict[str, str] = {
    "content-security-policy": "restringe orígenes de recursos (mitiga XSS)",
    "strict-transport-security": "fuerza HTTPS (mitiga downgrade)",
    "x-frame-options": "impide incrustación en iframes (mitiga clickjacking)",
    "x-content-type-options": "impide MIME-sniffing",
    "referrer-policy": "controla la información enviada en Referer",
    "permissions-policy": "limita APIs del navegador (cámara, geo...)",
}


@dataclass
class AuditResult:
    url: str
    status: int = 0
    headers: Dict[str, str] = field(default_factory=dict)
    findings: List[str] = field(default_factory=list)


def _fetch_headers(url: str, timeout: float = 8.0) -> tuple[int, Dict[str, str]]:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    ctx = ssl.create_default_context() if parsed.scheme == "https" else None
    conn_cls = http.client.HTTPSConnection if parsed.scheme == "https" else http.client.HTTPConnection
    conn = conn_cls(host, port, timeout=timeout, context=ctx)
    conn.request("GET", path, headers={"User-Agent": "sec-tool/httpaudit"})
    resp = conn.getresponse()
    headers = {k.lower(): v for k, v in resp.getheaders()}
    status = resp.status
    conn.close()
    return status, headers


def audit(url: str, timeout: float = 8.0) -> AuditResult:
    result = AuditResult(url=url)
    try:
        result.status, result.headers = _fetch_headers(url, timeout)
    except Exception as exc:  # noqa: BLE001 - report any fetch failure
        result.findings.append(f"no se pudo obtener la respuesta: {exc}")
        return result
    for header, why in CHECKLIST.items():
        value = result.headers.get(header)
        if value is None:
            result.findings.append(f"MISSING {header} — {why}")
        elif header == "content-security-policy" and "default-src" not in value:
            result.findings.append(f"DEBIL {header}: no define default-src")
        elif header == "strict-transport-security" and "max-age" not in value:
            result.findings.append(f"DEBIL {header}: sin max-age")
    if "server" in result.headers:
        result.findings.append(f"INFO: cabecera Server revela {result.headers['server']}")
    return result
