from unittest.mock import patch

from security_toolkit.httpaudit import audit, CHECKLIST


def test_missing_headers_flagged():
    # Respuesta sin ninguna cabecera de seguridad -> todas MISSING
    mock_resp = type("R", (), {"status": 200, "getheaders": lambda self: []})
    with patch("security_toolkit.httpaudit._fetch_headers", return_value=(200, {})):
        result = audit("https://ejemplo.com")
    assert len(result.findings) == len(CHECKLIST)  # +0 (no Server header)


def test_weak_csp_flagged():
    headers = {"content-security-policy": "script-src 'self'"}
    with patch("security_toolkit.httpaudit._fetch_headers", return_value=(200, headers)):
        result = audit("https://ejemplo.com")
    assert any("DEBIL content-security-policy" in f for f in result.findings)


def test_server_header_info():
    headers = {"server": "nginx/1.24"}
    with patch("security_toolkit.httpaudit._fetch_headers", return_value=(200, headers)):
        result = audit("https://ejemplo.com")
    assert any("Server revela" in f for f in result.findings)


def test_fetch_failure_reported():
    with patch(
        "security_toolkit.httpaudit._fetch_headers", side_effect=OSError("conexión rechazada")
    ):
        result = audit("https://ejemplo.com")
    assert result.findings
