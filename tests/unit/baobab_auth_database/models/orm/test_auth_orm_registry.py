"""Tests du registre ORM."""

from sqlalchemy import inspect

from baobab_auth_database.factories.sqlalchemy_engine_factory import (
    SqlAlchemyEngineFactory,
)
from baobab_auth_database.models.orm.auth_orm_registry import AuthOrmRegistry
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class TestAuthOrmRegistry:
    """Tests FEAT-002.1 — registre et création de schéma."""

    def test_FEAT_002_1_neuf_modeles_enregistres(self) -> None:
        assert len(AuthOrmRegistry.MODELS) == 10
        assert len(AuthOrmRegistry.table_names()) == 10

    def test_FEAT_002_1_create_all_sqlite(self) -> None:
        settings = AuthDatabaseSettings()
        engine = SqlAlchemyEngineFactory(settings).create()
        try:
            AuthOrmRegistry.create_all(engine)
            inspector = inspect(engine)
            tables = set(inspector.get_table_names())
            for name in AuthOrmRegistry.table_names():
                assert name in tables
        finally:
            AuthOrmRegistry.drop_all(engine)
            engine.dispose()
