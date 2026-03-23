import time
from decimal import Decimal
from typing import TypedDict

from sqlalchemy import select
from sqlalchemy.orm import Session

from mocks.htx.db.models import MockStub, Withdraw


class WithdrawData(TypedDict):
    currency: str
    amount: Decimal
    address: str
    chain: str
    address_tag: str
    fee: Decimal


class MockDataRepository:

    def __init__(self, db: Session) -> None:
        self._db = db

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

    def create_withdraw(self, data: WithdrawData) -> Withdraw:
        now_ms = int(time.time() * 1000)

        withdraw = Withdraw(
            type="withdraw",
            sub_type="onchain",
            currency=data["currency"],
            chain=data["chain"],
            chain_full_name=data["chain"],
            tx_hash="",
            amount=data["amount"],
            from_addr_tag="",
            address_id=0,
            address=data["address"],
            address_tag=data["address_tag"],
            fee=data["fee"],
            state="submitted",
            error_code=None,
            error_msg=None,
            created_at=now_ms,
            updated_at=now_ms,
            pass_at=None,
        )

        self._db.add(withdraw)
        self._db.flush()
        return withdraw
