from fastapi import FastAPI
from mocks.htx.api.htx import router as htx_router

from mocks.htx.config.settings import get_settings

settings = get_settings()

app = FastAPI(title="HTX Mock Service")
app.include_router(htx_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )