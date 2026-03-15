from pydantic import BaseModel, ValidationError

from clients.htx.auth import build_signed_params
from clients.htx.endpoints import (
    CREATE_WITHDRAW,
    GET_DEPOSIT_ADDRESS,
    GET_DEPOSIT_WITHDRAW_HISTORY,
    GET_ORDERBOOK,
)
from clients.htx.exceptions import HtxInvalidResponseError
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
from infrastructure.http.transport import HttpTransport



HUOBI_API_HOST = "api.huobi.pro"


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
        self.transport = HttpTransport(base_url=base_url, timeout=timeout)
        self.host = HUOBI_API_HOST

    def _make_request(
        self,
        method: str,
        path: str,
        query: dict | None = None,
        body: dict | None = None,
        headers: dict[str, str] | None = None,
        is_private: bool = False,
    ) -> dict:
        request_query = query.copy() if query else {}

        if is_private:
            request_query = build_signed_params(
                method=method,
                host=self.host,
                path=path,
                access_key=self.access_key,
                secret_key=self.secret_key,
                params=request_query,
            )

        response = self.transport.request(
            method=method,
            path=path,
            query=request_query,
            body=body,
            headers=headers,
        )
        return response.json()


    def _validate_response[ResponseModel: BaseModel](
        self,
        schema: type[ResponseModel],
        response_data: dict,
    ) -> ResponseModel:
        try:
            return schema.model_validate(response_data)
        except ValidationError as e:
            raise HtxInvalidResponseError(f"Invalid HTX response for {schema.__name__}: {e}") from e

    def _make_request_and_validate_response[RequestModel: BaseModel, ResponseModel: BaseModel](
        self,
        method: str,
        path: str,
        params: RequestModel,
        schema: type[ResponseModel],
        is_private: bool = False,
        by_alias: bool = False,
        send_as_body: bool = False,
    ) -> ResponseModel:
        response_data = self._make_request(
            method=method.upper(),
            path=path,
            query=params.model_dump(by_alias=by_alias, exclude_none=True) if not send_as_body else None,
            body=params.model_dump(by_alias=by_alias, exclude_none=True) if send_as_body else None,
            is_private=is_private,
        )
        return self._validate_response(schema=schema, response_data=response_data)



    def get_orderbook(self, params: OrderBookRequestParams) -> OrderBookResponse:
        return self._make_request_and_validate_response(method="GET", path=GET_ORDERBOOK, params=params, schema=OrderBookResponse)


    def get_deposit_address(
        self,
        params: DepositAddressRequestParams,
    ) -> DepositAddressResponse:
        return self._make_request_and_validate_response(method="GET",
            path=GET_DEPOSIT_ADDRESS,
            params=params,
            schema=DepositAddressResponse,
            is_private=True, )

    def get_withdraw_history(
        self,
        params: WithdrawHistoryRequestParams,
    ) -> WithdrawHistoryResponse:
        return self._make_request_and_validate_response(method="GET",
            path=GET_DEPOSIT_WITHDRAW_HISTORY,
            params=params,
            schema=WithdrawHistoryResponse,
            is_private=True,
            by_alias=True, )

    def create_withdraw(
        self,
        body: CreateWithdrawRequest,
    ) -> CreateWithdrawResponse:
        return self._make_request_and_validate_response(method="POST",
            path=CREATE_WITHDRAW,
            params=body,
            schema=CreateWithdrawResponse,
            is_private=True,
            by_alias=True,
            send_as_body=True, )

    def close(self) -> None:
        self.transport.close()
