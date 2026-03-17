from sqlalchemy.orm import Session

from mocks.htx.db.models import MockStub


class MockStubRepository:
    """Repository for reading mock stubs from the database."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_active_stubs(self, endpoint_key: str) -> list[type[MockStub]]:
        """
        Return all active stubs for a given endpoint.

        Stubs are ordered by priority (highest first) and then by id
        to keep deterministic ordering.
        """
        return (
            self._db.query(MockStub)
            .filter(
                MockStub.endpoint_key == endpoint_key,
                MockStub.is_active.is_(True),
            )
            .order_by(MockStub.priority.desc(), MockStub.id.asc())
            .all()
        )
