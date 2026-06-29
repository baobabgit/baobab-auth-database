"""Tests unitaires factories SQLAlchemy."""

from sqlalchemy import text
from sqlalchemy.orm import Session

from baobab_auth_database.factories.sqlalchemy_engine_factory import (
    SqlAlchemyEngineFactory,
)
from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class TestSqlAlchemyEngineFactory:
    """Tests FEAT-001.2 — engine factory."""

    def test_FEAT_001_2_create_engine_sqlite_memoire(self) -> None:
        settings = AuthDatabaseSettings()
        engine = SqlAlchemyEngineFactory(settings).create()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar_one()
        assert result == 1
        engine.dispose()

    def test_FEAT_001_2_create_engine_postgresql_pool(self) -> None:
        from unittest.mock import MagicMock, patch

        from pydantic import SecretStr

        settings = AuthDatabaseSettings(
            database_url=SecretStr("postgresql://user:pass@localhost:5432/auth"),
            pool_size=3,
            max_overflow=2,
        )
        with patch(
            "baobab_auth_database.factories.sqlalchemy_engine_factory.create_engine",
            return_value=MagicMock(),
        ) as mock_create:
            SqlAlchemyEngineFactory(settings).create()
        kwargs = mock_create.call_args.kwargs
        assert kwargs["pool_size"] == 3
        assert kwargs["max_overflow"] == 2

    def test_FEAT_001_2_session_factory_avec_engine_existant(self) -> None:
        settings = AuthDatabaseSettings()
        engine = SqlAlchemyEngineFactory(settings).create()
        factory = SqlAlchemySessionFactory(settings, engine=engine)
        assert factory.engine is engine
        factory.engine.dispose()

    """Tests FEAT-001.2 — session factory."""

    def test_FEAT_001_2_create_session_sqlite_memoire(self) -> None:
        settings = AuthDatabaseSettings()
        factory = SqlAlchemySessionFactory(settings)
        session: Session = factory.create()
        try:
            assert session.execute(text("SELECT 1")).scalar_one() == 1
        finally:
            session.close()
            factory.engine.dispose()
