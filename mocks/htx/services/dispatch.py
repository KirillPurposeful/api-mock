from typing import Any, Callable

from mocks.htx.db.models import MockMode
from mocks.htx.repositories.mock_mode import MockSettingsRepository
from mocks.htx.repositories.stubs import MockStubRepository
from mocks.htx.services.matcher import match_stub


class MockDispatchService:
    """
    Central service that decides whether to return real data
    from the client or mock data from the database.
    """

    def __init__(self, db) -> None:
        self._settings_repo = MockSettingsRepository(db)
        self._stubs_repo = MockStubRepository(db)

    def dispatch(
        self,
        endpoint_key: str,
        request_params: dict[str, Any],
        real_call: Callable[[], Any],
    ) -> Any:
        """
        endpoint_key: normalized endpoint identifier (e.g. 'orderbook')
        request_params: request query/body params as dict
        real_call: function that calls the real HTX client
        """

        mode = self._settings_repo.get_mode()

        if mode == MockMode.REAL:
            return real_call()

        stubs = self._stubs_repo.get_active_stubs(endpoint_key)

        stub = match_stub(stubs, request_params)

        if stub is None:
            raise RuntimeError(
                f"No mock stub matched for endpoint '{endpoint_key}' with params {request_params}"
            )

        return stub.response_body