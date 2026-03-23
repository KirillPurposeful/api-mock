from decimal import Decimal

from pydantic import BaseModel, Field


class OrderBookRequestParams(BaseModel):
    symbol: str
    type: str
    depth: int | None = None


class OrderBookData(BaseModel):
    bids: list[list[Decimal]]
    asks: list[list[Decimal]]
    ts: int
    version: int


class OrderBookResponse(BaseModel):
    status: str
    ch: str
    ts: int
    tick: OrderBookData


class DepositAddressRequestParams(BaseModel):
    currency: str


class DepositAddressItem(BaseModel):
    user_id: int = Field(alias="userId")
    currency: str
    address: str
    address_tag: str = Field(alias="addressTag")
    chain: str


class DepositAddressResponse(BaseModel):
    code: int
    message: str | None = None
    data: list[DepositAddressItem]


class WithdrawHistoryRequestParams(BaseModel):
    currency: str | None = None
    type: str
    from_: int | None = Field(default=None, alias="from")
    size: int | None = None
    direct: str | None = None


class WithdrawHistoryItem(BaseModel):
    id: int
    type: str
    sub_type: str = Field(alias="sub-type")
    currency: str
    chain: str
    chain_full_name: str = Field(alias="chain-full-name")
    tx_hash: str = Field(alias="tx-hash")
    amount: Decimal
    from_addr_tag: str = Field(alias="from-addr-tag")
    address_id: int = Field(alias="address-id")
    address: str
    address_tag: str = Field(alias="address-tag")
    fee: Decimal
    state: str
    error_code: str | None = Field(default=None, alias="error-code")
    error_msg: str | None = Field(default=None, alias="error-msg")
    created_at: int = Field(alias="created-at")
    updated_at: int = Field(alias="updated-at")
    pass_at: int | None = Field(default=None, alias="pass-at")


class WithdrawHistoryResponse(BaseModel):
    status: str
    data: list[WithdrawHistoryItem]


class CreateWithdrawRequest(BaseModel):
    address: str
    amount: Decimal
    currency: str
    chain: str | None = None
    addr_tag: str | None = Field(default=None, alias="addr-tag")
    fee: Decimal | None = None
    client_order_id: str | None = Field(default=None, alias="client-order-id")


class CreateWithdrawResponse(BaseModel):
    status: str
    data: int