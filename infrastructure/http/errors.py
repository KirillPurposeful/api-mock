class HttpError(Exception):
    """Transport-level error (non-2xx, timeout, connection failure)."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
