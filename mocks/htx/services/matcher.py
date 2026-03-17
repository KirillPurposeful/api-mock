

from typing import Any

from mocks.htx.db.models import MockStub


def match_stub(stubs: list[MockStub], request_params: dict[str, Any]) -> MockStub | None:
    """
    Find the first stub whose matcher conditions are satisfied by request_params.

    A stub matches when all keys in stub.matcher exist in request_params
    and have equal values.
    """

    for stub in stubs:
        matcher = stub.matcher or {}

        is_match = True

        for key, value in matcher.items():
            if request_params.get(key) != value:
                is_match = False
                break

        if is_match:
            return stub

    return None