"""JWT inspection: decode header/payload and detect `alg:none` (weak signature)."""
from __future__ import annotations

import base64
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List


def _b64url_decode(segment: str) -> bytes:
    padding = "=" * (-len(segment) % 4)
    return base64.urlsafe_b64decode(segment + padding)


@dataclass
class JWTResult:
    token: str
    header: Dict[str, Any] = field(default_factory=dict)
    payload: Dict[str, Any] = field(default_factory=dict)
    alg: str = ""
    issues: List[str] = field(default_factory=list)
    valid_structure: bool = False


def inspect(token: str) -> JWTResult:
    """Decode (but do NOT verify signature) a JWT for inspection purposes."""
    result = JWTResult(token=token)
    parts = token.split(".")
    if len(parts) != 3:
        result.issues.append("el token no tiene 3 segmentos (header.payload.signature)")
        return result
    try:
        result.header = json.loads(_b64url_decode(parts[0]))
        result.payload = json.loads(_b64url_decode(parts[1]))
        result.valid_structure = True
    except Exception as exc:  # noqa: BLE001
        result.issues.append(f"no se pudo decodificar: {exc}")
        return result

    result.alg = result.header.get("alg", "")
    if result.alg.lower() == "none":
        result.issues.append(
            "alg:none — firma desactivada (CVE-2015-9235). Cualquier payload firmado con "
            "alg:none se acepta como válido por servidores mal configurados."
        )
    if "exp" in result.payload:
        import time

        exp = result.payload["exp"]
        if isinstance(exp, (int, float)) and exp < time.time():
            result.issues.append(f"token expirado (exp={exp})")
    if "iss" not in result.payload:
        result.issues.append("sin reclamación 'iss' (emisor no verificado)")
    return result
