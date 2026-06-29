"""Tests AuthCatalogBootstrap."""

from pathlib import Path

import pytest
from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
from baobab_auth_core.domain.value_objects.role_name import RoleName
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


@pytest.fixture
def migrated_session_factory(tmp_path: Path) -> SqlAlchemySessionFactory:
    """Factory SQLite migrée prête pour le bootstrap.

    :param tmp_path: Répertoire temporaire pytest.
    :returns: Factory avec schéma Alembic appliqué.
    """
    db_file = tmp_path / "bootstrap.db"
    settings = AuthDatabaseSettings(
        database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
    )
    AuthDatabaseMigrator(settings).upgrade_head()
    return SqlAlchemySessionFactory(settings)


class TestAuthCatalogBootstrap:
    """Tests FEAT-005.2 — bootstrap catalogue core."""

    def test_FEAT_005_2_seed_permissions_and_roles(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        """Premier appel insère le catalogue DefaultAuthCatalog."""
        catalog = DefaultAuthCatalog()
        AuthCatalogBootstrap(migrated_session_factory, catalog=catalog).run()

        with SqlAlchemyAuthUnitOfWork(migrated_session_factory) as uow:
            assert len(uow.permissions.list_all()) == len(catalog.permissions())
            assert len(uow.roles.list_all()) == len(catalog.roles())
            assert uow.roles.get_by_name(RoleName("ADMIN")) is not None

    def test_FEAT_005_2_idempotent_second_run(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        """Second appel sans doublon ni erreur d'unicité."""
        bootstrap = AuthCatalogBootstrap(migrated_session_factory)
        bootstrap.run()
        bootstrap.run()

        catalog = DefaultAuthCatalog()
        with SqlAlchemyAuthUnitOfWork(migrated_session_factory) as uow:
            assert len(uow.permissions.list_all()) == len(catalog.permissions())
            assert len(uow.roles.list_all()) == len(catalog.roles())
