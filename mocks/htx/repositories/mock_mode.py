from sqlalchemy.orm import Session

from mocks.htx.db.models import MockSettings, MockMode


class MockSettingsRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_mode(self) -> MockMode:
        settings = self._db.query(MockSettings).order_by(MockSettings.id.asc()).first()
        if settings is None:
            return MockMode.REAL
        return MockMode(settings.mode)

