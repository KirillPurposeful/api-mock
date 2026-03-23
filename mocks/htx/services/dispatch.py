from typing import Any

from mocks.htx.db.models import MockStub
from mocks.htx.exceptions import MockStubErrorStatusError, MockStubNotFoundError
from mocks.htx.repositories.mock_data import MockDataRepository


def _match_stub(stubs: list[MockStub], request_params: dict[str, Any]) -> MockStub | None:
    for stub in stubs:
        matcher: dict[str, Any] = stub.matcher or {}

        is_match = True
        for key, value in matcher.items():
            if request_params.get(key) != value:
                is_match = False
                break

        if is_match:
            return stub

    return None


class MockDispatchService:

    def __init__(self, repo: MockDataRepository) -> None:
        self._stubs_repo = repo

    def dispatch(
        self,
        endpoint_key: str,
        request_params: dict[str, Any],
    ) -> dict[str, object]:

        stubs = self._stubs_repo.get_active_stubs(endpoint_key)

        stub = _match_stub(stubs, request_params)

        if stub is None:
            raise MockStubNotFoundError(endpoint_key, request_params)

        if stub.response_status < 200 or stub.response_status >= 300:
            raise MockStubErrorStatusError(endpoint_key, stub.response_status, stub.response_body)

        return stub.response_body
