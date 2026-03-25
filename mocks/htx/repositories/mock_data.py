from sqlalchemy import select
from sqlalchemy.orm import Session

from mocks.htx.db.models import MockStub, Withdraw



class MockDataRepository:

    def __init__(self, db: Session) -> None:
        self._db = db

    def commit(self) -> None:
        self._db.commit()

    def get_active_stubs(self, endpoint_key: str) -> list[MockStub]:
        stmt = (
            select(MockStub)
            .where(
                MockStub.endpoint_key == endpoint_key,
                MockStub.is_active.is_(True),
            )
            .order_by(MockStub.priority.desc(), MockStub.id.asc())
        )
        return list(self._db.execute(stmt).scalars().all())

    def save_withdraw(self,
            withdraw: Withdraw) -> Withdraw:
        self._db.add(withdraw)
        self._db.flush()
        return withdraw
