

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from clients.htx.client import HtxClient
from clients.htx.schemas import (
    CreateWithdrawRequest,
    CreateWithdrawResponse,
    DepositAddressRequestParams,
    DepositAddressResponse,
    OrderBookRequestParams,
    OrderBookResponse,
    WithdrawHistoryRequestParams,
    WithdrawHistoryResponse,
)
from mocks.htx.config.settings import get_settings
from mocks.htx.db.session import get_db_session
from mocks.htx.services.dispatch import MockDispatchService

router = APIRouter()


@router.get("/market/depth", response_model=OrderBookResponse)
def get_orderbook(
    params: OrderBookRequestParams = Depends(),
    db: Session = Depends(get_db_session),
) -> OrderBookResponse | dict:
    settings = get_settings()
    client = HtxClient(
        base_url=settings.htx_base_url,
        access_key=settings.htx_access_key,
        secret_key=settings.htx_secret_key,
    )
    dispatch_service = MockDispatchService(db)

    try:
        response = dispatch_service.dispatch(
            endpoint_key="orderbook",
            request_params=params.model_dump(exclude_none=True),
            real_call=lambda: client.get_orderbook(params),
        )
    finally:
        client.close()

    return response


@router.get("/v2/account/deposit/address", response_model=DepositAddressResponse)
def get_deposit_address(
    params: DepositAddressRequestParams = Depends(),
    db: Session = Depends(get_db_session),
) -> DepositAddressResponse | dict:
    settings = get_settings()
    client = HtxClient(
        base_url=settings.htx_base_url,
        access_key=settings.htx_access_key,
        secret_key=settings.htx_secret_key,
    )
    dispatch_service = MockDispatchService(db)

    try:
        response = dispatch_service.dispatch(
            endpoint_key="deposit_address",
            request_params=params.model_dump(exclude_none=True),
            real_call=lambda: client.get_deposit_address(params),
        )
    finally:
        client.close()

    return response


@router.get("/v1/query/deposit-withdraw", response_model=WithdrawHistoryResponse)
def get_withdraw_history(
    params: WithdrawHistoryRequestParams = Depends(),
    db: Session = Depends(get_db_session),
) -> WithdrawHistoryResponse | dict:
    settings = get_settings()
    client = HtxClient(
        base_url=settings.htx_base_url,
        access_key=settings.htx_access_key,
        secret_key=settings.htx_secret_key,
    )
    dispatch_service = MockDispatchService(db)

    try:
        response = dispatch_service.dispatch(
            endpoint_key="withdraw_history",
            request_params=params.model_dump(by_alias=True, exclude_none=True),
            real_call=lambda: client.get_withdraw_history(params),
        )
    finally:
        client.close()

    return response


@router.post("/v1/dw/withdraw/api/create", response_model=CreateWithdrawResponse)
def create_withdraw(
    body: CreateWithdrawRequest,
    db: Session = Depends(get_db_session),
) -> CreateWithdrawResponse | dict:
    settings = get_settings()
    client = HtxClient(
        base_url=settings.htx_base_url,
        access_key=settings.htx_access_key,
        secret_key=settings.htx_secret_key,
    )
    dispatch_service = MockDispatchService(db)

    try:
        response = dispatch_service.dispatch(
            endpoint_key="create_withdraw",
            request_params=body.model_dump(by_alias=True, exclude_none=True),
            real_call=lambda: client.create_withdraw(body),
        )
    finally:
        client.close()

    return response