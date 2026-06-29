"""Fixtures pytest partagées."""

from collections.abc import Iterator
from datetime import UTC, datetime

import pytest
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from baobab_auth_database.factories.sqlalchemy_engine_factory import (
    SqlAlchemyEngineFactory,
)
from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


@pytest.fixture
def now_utc() -> datetime:
    """Horodatage UTC fixe pour les tests de mappers.

    :returns: Datetime timezone-aware reproductible.
    """
    return datetime(2026, 1, 15, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def sqlite_engine() -> Iterator[Engine]:
    """Engine SQLite mémoire avec schéma auth créé.

    :yields: Engine SQLAlchemy prêt pour les tests repositories.
    """
    settings = AuthDatabaseSettings()
    engine = SqlAlchemyEngineFactory(settings).create()
    AuthOrmBase.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(sqlite_engine: Engine) -> Iterator[Session]:
    """Session SQLAlchemy avec rollback implicite en fin de test.

    :param sqlite_engine: Engine SQLite mémoire.
    :yields: Session active.
    """
    settings = AuthDatabaseSettings()
    session = SqlAlchemySessionFactory(settings, engine=sqlite_engine).create()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
