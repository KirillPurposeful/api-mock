from fastapi import APIRouter, Depends

from app.providers import get_htx_service
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
from clients.htx.client import HtxClient
from mocks.htx.services.htx_mock_service import HtxMockService

router = APIRouter()


@router.get("/market/depth", response_model=OrderBookResponse)
def get_orderbook(
    params: OrderBookRequestParams = Depends(),
    service: HtxClient | HtxMockService = Depends(get_htx_service),
):
    return service.get_orderbook(params)


@router.get("/v2/account/deposit/address", response_model=DepositAddressResponse)
def get_deposit_address(
    params: DepositAddressRequestParams = Depends(),
    service: HtxClient | HtxMockService = Depends(get_htx_service),
):
    return service.get_deposit_address(params)


@router.get("/v1/query/deposit-withdraw", response_model=WithdrawHistoryResponse)
def get_withdraw_history(
    params: WithdrawHistoryRequestParams = Depends(),
    service: HtxClient | HtxMockService = Depends(get_htx_service),
):
    return service.get_withdraw_history(params)


@router.post("/v1/dw/withdraw/api/create", response_model=CreateWithdrawResponse)
def create_withdraw(
    body: CreateWithdrawRequest,
    service: HtxClient | HtxMockService = Depends(get_htx_service),
):
    return service.create_withdraw(body)
