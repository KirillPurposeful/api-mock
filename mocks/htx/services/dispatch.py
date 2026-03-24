from mocks.htx.exceptions import MockStubErrorStatusError, MockStubNotFoundError
from mocks.htx.repositories.mock_data import MockDataRepository
from mocks.htx.services.matcher import match_stub


class MockDispatchService:

    def __init__(self, repo: MockDataRepository) -> None:
        self._stubs_repo = repo

    def dispatch(
        self,
        endpoint_key: str,
        request_params: dict[str, object],
    ) -> dict[str, object]:

        stubs = self._stubs_repo.get_active_stubs(endpoint_key)

        stub = match_stub(stubs, request_params)

        if stub is None:
            raise MockStubNotFoundError(endpoint_key, request_params)

        if stub.response_status < 200 or stub.response_status >= 300:
            raise MockStubErrorStatusError(endpoint_key, stub.response_status, stub.response_body)

        return stub.response_body
