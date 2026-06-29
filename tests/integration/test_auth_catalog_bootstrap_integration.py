"""Tests d'intégration bootstrap catalogue sur SQLite."""

from pathlib import Path

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
from pydantic import SecretStr

from baobab_auth_database.bootstrap.auth_catalog_bootstrap import AuthCatalogBootstrap
from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.migrations.auth_database_migrator import AuthDatabaseMigrator
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings
from baobab_auth_database.unit_of_work.sqlalchemy_auth_unit_of_work import (
    SqlAlchemyAuthUnitOfWork,
)


class TestAuthCatalogBootstrapIntegration:
    """Intégration FEAT-005.2 — bootstrap SQLite migré."""

    def test_FEAT_005_2_bootstrap_after_upgrade_is_idempotent(
        self, tmp_path: Path
    ) -> None:
        db_file = tmp_path / "integration.db"
        settings = AuthDatabaseSettings(
            database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
        )
        AuthDatabaseMigrator(settings).upgrade_head()
        session_factory = SqlAlchemySessionFactory(settings)
        bootstrap = AuthCatalogBootstrap(session_factory)

        bootstrap.run()
        bootstrap.run()

        catalog = DefaultAuthCatalog()
        with SqlAlchemyAuthUnitOfWork(session_factory) as uow:
            permissions = uow.permissions.list_all()
            roles = uow.roles.list_all()
            assert len(permissions) == len(catalog.permissions())
            assert len(roles) == len(catalog.roles())
