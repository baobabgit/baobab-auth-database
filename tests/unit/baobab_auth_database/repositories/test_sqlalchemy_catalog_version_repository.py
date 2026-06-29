"""Tests SqlAlchemyCatalogVersionRepository."""

from pathlib import Path

import pytest
from pydantic import SecretStr

from baobab_auth_database.bootstrap.auth_catalog_bootstrap import AuthCatalogBootstrap
from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.migrations.auth_database_migrator import AuthDatabaseMigrator
from baobab_auth_database.repositories.sqlalchemy_catalog_version_repository import (
    SqlAlchemyCatalogVersionRepository,
)
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


@pytest.fixture
def migrated_session_factory(tmp_path: Path) -> SqlAlchemySessionFactory:
    db_file = tmp_path / "catalog_version.db"
    settings = AuthDatabaseSettings(
        database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
    )
    AuthDatabaseMigrator(settings).upgrade_head()
    return SqlAlchemySessionFactory(settings)


class TestSqlAlchemyCatalogVersionRepository:
    """Tests FEAT-006.4 — versions catalogue."""

    def test_FEAT_006_4_bootstrap_records_version(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        result = AuthCatalogBootstrap(migrated_session_factory).run()
        assert result.version_recorded is True

        session = migrated_session_factory.create()
        try:
            repo = SqlAlchemyCatalogVersionRepository(session)
            latest = repo.get_latest()
        finally:
            session.close()

        assert latest is not None
        assert latest.compat_profile == "core_051"
        assert len(latest.catalog_checksum) == 64

    def test_FEAT_006_4_list_all_ordered(
        self, migrated_session_factory: SqlAlchemySessionFactory
    ) -> None:
        bootstrap = AuthCatalogBootstrap(migrated_session_factory)
        bootstrap.run()
        bootstrap.run()

        session = migrated_session_factory.create()
        try:
            records = SqlAlchemyCatalogVersionRepository(session).list_all()
        finally:
            session.close()

        assert len(records) == 2
        assert records[0].applied_at >= records[1].applied_at
