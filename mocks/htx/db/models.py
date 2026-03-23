from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MockMode(str, Enum):
    REAL = "real"
    MOCK = "mock"



class MockSettings(Base):
    __tablename__ = "mock_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mode: Mapped[str] = mapped_column(String(16), nullable=False, default=MockMode.REAL.value)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class MockStub(Base):
    __tablename__ = "mock_stubs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    endpoint_key: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    matcher: Mapped[dict] = mapped_column(JSONB, nullable=False)
    response_status: Mapped[int] = mapped_column(Integer, nullable=False, default=200)
    response_body: Mapped[dict] = mapped_column(JSONB, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

class Withdraw(Base):
    __tablename__ = "withdraws"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    sub_type: Mapped[str] = mapped_column(String, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    chain: Mapped[str] = mapped_column(String, nullable=False)
    chain_full_name: Mapped[str] = mapped_column(String, nullable=False)
    tx_hash: Mapped[str] = mapped_column(String, nullable=False)

    amount: Mapped[Decimal] = mapped_column(Numeric, nullable=False)
    fee: Mapped[Decimal] = mapped_column(Numeric, nullable=False)

    from_addr_tag: Mapped[str] = mapped_column(String, nullable=False)
    address_id: Mapped[int] = mapped_column(Integer, nullable=False)
    address: Mapped[str] = mapped_column(String, nullable=False)
    address_tag: Mapped[str] = mapped_column(String, nullable=False)

    state: Mapped[str] = mapped_column(String, nullable=False)

    error_code: Mapped[str | None] = mapped_column(String, nullable=True)
    error_msg: Mapped[str | None] = mapped_column(String, nullable=True)

    created_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    updated_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    pass_at: Mapped[int | None] = mapped_column(BigInteger, nullable=True)