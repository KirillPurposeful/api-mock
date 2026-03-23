from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.htx import router as htx_router
from mocks.htx.exceptions import MockStubErrorStatusError, MockStubNotFoundError

app = FastAPI(title="HTX Mock Service")
app.include_router(htx_router, tags=["HTX"])


@app.exception_handler(MockStubNotFoundError)
def handle_mock_stub_not_found(_request: Request, exc: MockStubNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(MockStubErrorStatusError)
def handle_mock_stub_error_status(_request: Request, exc: MockStubErrorStatusError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.body)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )