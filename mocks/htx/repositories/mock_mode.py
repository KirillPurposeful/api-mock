from sqlalchemy import select
from sqlalchemy.orm import Session

from mocks.htx.db.models import MockSettings, MockMode

# TODO: кароч как пофиксишь таблицу мок мод тут тоже нужно код фиксануть
class MockSettingsRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_mode(self) -> MockMode:
        stmt = select(MockSettings).order_by(MockSettings.id.asc())
        settings = self._db.execute(stmt).scalars().first()
        if settings is None:
            return MockMode.REAL
        return MockMode(settings.mode)
