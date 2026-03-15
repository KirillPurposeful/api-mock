import base64
import hashlib
import hmac
from datetime import datetime, timezone
from urllib.parse import urlencode


def _build_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def _build_auth_params(api_key: str) -> dict[str, str]:
    return {
        "AccessKeyId": api_key,
        "SignatureMethod": "HmacSHA256",
        "SignatureVersion": "2",
        "Timestamp": _build_timestamp(),
    }


def _sign_request(
    method: str,
    host: str,
    path: str,
    params: dict,
    secret_key: str,
) -> str:
    sorted_params = sorted(params.items(), key=lambda item: item[0])
    encoded_params = urlencode(sorted_params)
    payload = "\n".join(
        [
            method.upper(),
            host.lower(),
            path,
            encoded_params,
        ]
    )

    digest = hmac.new(
        secret_key.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    return base64.b64encode(digest).decode("utf-8")


def build_signed_params(
    method: str,
    host: str,
    path: str,
    access_key: str,
    secret_key: str,
    params: dict | None = None,
) -> dict:
    signed_params = _build_auth_params(access_key)

    if params:
        signed_params.update(params)

    signed_params["Signature"] = _sign_request(
        method=method,
        host=host,
        path=path,
        params=signed_params,
        secret_key=secret_key,
    )

    return signed_params
