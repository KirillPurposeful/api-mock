from mocks.htx.db.models import MockStub


def match_stub(stubs: list[MockStub], request_params: dict[str, object]) -> MockStub | None:

    for stub in stubs:
        expected_params = stub.matcher or {}

        if all(request_params.get(key) == value for key, value in expected_params.items()):
            return stub

    return None