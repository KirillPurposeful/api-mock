class MockStubNotFoundError(Exception):

    def __init__(self, endpoint_key: str, params: dict) -> None:
        self.endpoint_key = endpoint_key
        self.params = params
        super().__init__(f"No mock stub matched for '{endpoint_key}' with params {params}")


class MockStubErrorStatusError(Exception):

    def __init__(self, endpoint_key: str, status_code: int, body: dict) -> None:
        self.endpoint_key = endpoint_key
        self.status_code = status_code
        self.body = body
        super().__init__(f"Mock stub for '{endpoint_key}' returned error status {status_code}")

