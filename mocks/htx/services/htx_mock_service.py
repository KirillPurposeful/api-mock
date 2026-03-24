from decimal import Decimal

from pydantic import BaseModel, ValidationError
from sqlalchemy.orm import Session

from app.schemas.htx import (
    CreateWithdrawRequest,
    CreateWithdrawResponse,
    DepositAddressRequestParams,
    DepositAddressResponse,
    OrderBookRequestParams,
    OrderBookResponse,
    WithdrawHistoryRequestParams,
    WithdrawHistoryResponse,
)
from mocks.htx.repositories.mock_data import MockDataRepository, WithdrawData
from mocks.htx.services.dispatch import MockDispatchService
from mocks.htx.services.endpoint_keys import DEPOSIT_ADDRESS, ORDERBOOK, WITHDRAW_HISTORY


class HtxMockService:


    def __init__(self, db: Session) -> None:
        self._repo = MockDataRepository(db)
        self._dispatch = MockDispatchService(self._repo)

    def _dispatch_and_validate[T: BaseModel](
        self,
        endpoint_key: str,
        request_params: dict[str, object],
        schema: type[T],
    ) -> T:
        body = self._dispatch.dispatch(
            endpoint_key=endpoint_key,
            request_params=request_params,
        )

        try:
            return schema.model_validate(body)
        except ValidationError as e:
            raise ValueError(
                f"Mock stub for '{endpoint_key}' contains invalid response_body: {e}"
            ) from e

    def get_orderbook(self, params: OrderBookRequestParams) -> OrderBookResponse:
        return self._dispatch_and_validate(
            endpoint_key=ORDERBOOK,
            request_params=params.model_dump(exclude_none=True),
            schema=OrderBookResponse,
        )

    def get_deposit_address(self, params: DepositAddressRequestParams) -> DepositAddressResponse:
        return self._dispatch_and_validate(
            endpoint_key=DEPOSIT_ADDRESS,
            request_params=params.model_dump(exclude_none=True),
            schema=DepositAddressResponse,
        )

    def get_withdraw_history(self, params: WithdrawHistoryRequestParams) -> WithdrawHistoryResponse:
        return self._dispatch_and_validate(
            endpoint_key=WITHDRAW_HISTORY,
            request_params=params.model_dump(by_alias=True, exclude_none=True),
            schema=WithdrawHistoryResponse,
        )


    def create_withdraw(self, body: CreateWithdrawRequest) -> CreateWithdrawResponse:
        data: WithdrawData = {
            "currency": body.currency,
            "amount": body.amount,
            "address": body.address,
            "chain": body.chain or "",
            "address_tag": body.addr_tag or "",
            "fee": body.fee or Decimal("0"),
        }
        withdraw = self._repo.create_withdraw(data)
        self._repo.commit()

        return CreateWithdrawResponse(status="ok", data=withdraw.id)


