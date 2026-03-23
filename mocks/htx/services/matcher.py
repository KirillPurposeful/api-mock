from typing import Any

from mocks.htx.db.models import MockStub


# TODO: хм матчер стаб интересно
def match_stub(stubs: list[MockStub], request_params: dict[str, Any]) -> MockStub | None:
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