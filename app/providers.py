from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from clients.htx.client import HtxClient
from config.settings import get_settings
from mocks.htx.db.models import MockMode
from mocks.htx.db.session import get_db
from mocks.htx.repositories.mock_mode import MockSettingsRepository
from mocks.htx.services.htx_mock_service import HtxMockService


def get_htx_service(db: Session = Depends(get_db)) -> Generator[HtxClient | HtxMockService, None, None]:
    mode = MockSettingsRepository(db).get_mode()

    if mode == MockMode.MOCK:
        yield HtxMockService(db)
        return

    settings = get_settings()
    client = HtxClient(
        base_url=settings.htx_base_url,
        access_key=settings.htx_access_key,
        secret_key=settings.htx_secret_key,
    )
    try:
        yield client
    finally:
        client.close()
