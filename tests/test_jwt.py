import base64
import json

from security_toolkit.jwt import inspect


def _make_token(header, payload, sig=b"firma"):
    def enc(obj):
        raw = obj if isinstance(obj, bytes) else json.dumps(obj).encode()
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

    return f"{enc(header)}.{enc(payload)}.{enc(sig)}"


def test_decodes_valid_jwt():
    token = _make_token({"alg": "HS256", "typ": "JWT"}, {"sub": "123", "name": "ana"})
    result = inspect(token)
    assert result.valid_structure
    assert result.alg == "HS256"
    assert result.payload["sub"] == "123"


def test_alg_none_detected():
    token = _make_token({"alg": "none", "typ": "JWT"}, {"sub": "admin"})
    result = inspect(token)
    assert any("alg:none" in issue for issue in result.issues)


def test_malformed_token():
    result = inspect("no-parece-jwt")
    assert not result.valid_structure
    assert result.issues


def test_expired_detected():
    token = _make_token({"alg": "HS256"}, {"exp": 0})
    result = inspect(token)
    assert any("expirado" in issue for issue in result.issues)


def test_missing_iss():
    token = _make_token({"alg": "HS256"}, {"sub": "123"})
    result = inspect(token)
    assert any("iss" in issue for issue in result.issues)
