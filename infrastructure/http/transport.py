import requests

from infrastructure.http.errors import HttpError


class HttpTransport:
    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
    ):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()

    def request(
        self,
        method: str,
        path: str,
        query: dict | None = None,
        body: dict | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:

        url = f"{self._base_url}{path}"

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=query,
                json=body,
                headers=headers,
                timeout=self._timeout,
            )
        except requests.exceptions.RequestException as exc:
            raise HttpError(f"Connection error: {method} {path}") from exc

        if response.status_code >= 400:
            raise HttpError(
                f"HTTP {response.status_code}: {method} {path} - {response.text}",
                status_code=response.status_code,
            )

        return response

    def close(self) -> None:
        self._session.close()
