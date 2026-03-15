class HtxClientError(Exception):
    """Base HTX client error."""


class HtxAPIError(HtxClientError):
    """HTX returned an API-level error."""

    def __init__(self, err_code: str, err_msg: str) -> None:
        super().__init__(f"{err_code}: {err_msg}")
        self.err_code = err_code
        self.err_msg = err_msg


class HtxInvalidResponseError(HtxClientError):
    """HTX returned an unexpected response format."""