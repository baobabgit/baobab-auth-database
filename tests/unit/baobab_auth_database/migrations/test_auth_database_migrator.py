"""Tests du migrateur Alembic."""

from pathlib import Path

import pytest
from pydantic import SecretStr

from baobab_auth_database.migrations.auth_database_migrator import AuthDatabaseMigrator
from baobab_auth_database.migrations.migration_orm_consistency_checker import (
    MigrationOrmConsistencyChecker,
)
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


@pytest.fixture
def sqlite_settings(tmp_path: Path) -> AuthDatabaseSettings:
    db_file = tmp_path / "auth.db"
    return AuthDatabaseSettings(
        database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
    )


class TestAuthDatabaseMigrator:
    """Tests FEAT-002.2 — migrations Alembic."""

    def test_FEAT_002_2_upgrade_head_downgrade_base(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        migrator = AuthDatabaseMigrator(sqlite_settings)
        assert migrator.current_revision() is None

        migrator.upgrade_head()
        assert migrator.current_revision() == "0001"

        migrator.downgrade_base()
        assert migrator.current_revision() is None

    def test_FEAT_002_2_history_contient_0001(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        migrator = AuthDatabaseMigrator(sqlite_settings)
        history = migrator.history_ids()
        assert history == ("0001",)

    def test_FEAT_002_2_config_property(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        migrator = AuthDatabaseMigrator(sqlite_settings)
        assert migrator.config.get_main_option("sqlalchemy.url") == (
            sqlite_settings.resolved_database_url()
        )

    def test_FEAT_002_2_coherence_apres_upgrade(
        self, sqlite_settings: AuthDatabaseSettings
    ) -> None:
        migrator = AuthDatabaseMigrator(sqlite_settings)
        migrator.upgrade_head()
        engine = migrator.create_engine()
        try:
            MigrationOrmConsistencyChecker().assert_consistent(engine)
        finally:
            engine.dispose()
