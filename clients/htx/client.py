import requests
from pydantic import BaseModel

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
from clients.htx.auth import build_signed_params
from clients.htx.endpoints import (
    CREATE_WITHDRAW,
    GET_DEPOSIT_ADDRESS,
    GET_DEPOSIT_WITHDRAW_HISTORY,
    GET_ORDERBOOK,
)
from clients.htx.exceptions import HtxAPIError


HUOBI_API_HOST = "api.huobi.pro"


def _check_htx_response(data: dict) -> None:
    if data.get("status") == "error":
        raise HtxAPIError(
            err_code=data.get("err-code", "htx-error"),
            err_msg=data.get("err-msg", "HTX returned an error response"),
        )

    if "code" in data and data["code"] != 200:
        raise HtxAPIError(
            err_code=str(data["code"]),
            err_msg=data.get("message", "HTX returned an error response"),
        )


class HtxClient:
    def __init__(
        self,
        base_url: str,
        access_key: str,
        secret_key: str,
        timeout: float = 10.0,
    ) -> None:
        self.access_key = access_key
        self.secret_key = secret_key
        self.host = HUOBI_API_HOST
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()

    def _sign(self, method: str, path: str, params: dict) -> dict:
        return build_signed_params(
            method=method,
            host=self.host,
            path=path,
            access_key=self.access_key,
            secret_key=self.secret_key,
            params=params,
        )

    def _get(self, path: str, query: dict, schema: type[BaseModel]) -> BaseModel:
        response = self._session.get(f"{self._base_url}{path}", params=query, timeout=self._timeout)
        response.raise_for_status()
        data = response.json()
        _check_htx_response(data)
        return schema.model_validate(data)

    def _post(self, path: str, body: dict, schema: type[BaseModel]) -> BaseModel:
        response = self._session.post(f"{self._base_url}{path}", json=body, timeout=self._timeout)
        response.raise_for_status()
        data = response.json()
        _check_htx_response(data)
        return schema.model_validate(data)

    def get_orderbook(self, params: OrderBookRequestParams) -> OrderBookResponse:
        return self._get(GET_ORDERBOOK, params.model_dump(exclude_none=True), OrderBookResponse)

    def get_deposit_address(self, params: DepositAddressRequestParams) -> DepositAddressResponse:
        query = self._sign("GET", GET_DEPOSIT_ADDRESS, params.model_dump(exclude_none=True))
        return self._get(GET_DEPOSIT_ADDRESS, query, DepositAddressResponse)

    def get_withdraw_history(self, params: WithdrawHistoryRequestParams) -> WithdrawHistoryResponse:
        query = self._sign("GET", GET_DEPOSIT_WITHDRAW_HISTORY, params.model_dump(by_alias=True, exclude_none=True))
        return self._get(GET_DEPOSIT_WITHDRAW_HISTORY, query, WithdrawHistoryResponse)

    def create_withdraw(self, body: CreateWithdrawRequest) -> CreateWithdrawResponse:
        query = self._sign("POST", CREATE_WITHDRAW, body.model_dump(by_alias=True, exclude_none=True))
        return self._post(CREATE_WITHDRAW, query, CreateWithdrawResponse)

    def close(self) -> None:
        self._session.close()
