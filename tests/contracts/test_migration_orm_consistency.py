"""Tests contrat cohérence migration ↔ modèles ORM."""

from pathlib import Path

import pytest
from pydantic import SecretStr
from sqlalchemy import text

from baobab_auth_database.migrations.auth_database_migrator import AuthDatabaseMigrator
from baobab_auth_database.migrations.migration_orm_consistency_checker import (
    MigrationOrmConsistencyChecker,
    MigrationOrmMismatch,
)
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class TestMigrationOrmConsistency:
    """Tests FEAT-002.3 — harness cohérence schéma."""

    def test_FEAT_002_3_aucun_ecart_apres_migration(self, tmp_path: Path) -> None:
        db_file = tmp_path / "contract.db"
        settings = AuthDatabaseSettings(
            database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
        )
        migrator = AuthDatabaseMigrator(settings)
        migrator.upgrade_head()
        engine = migrator.create_engine()
        try:
            mismatches = MigrationOrmConsistencyChecker().check(engine)
            assert mismatches == ()
        finally:
            engine.dispose()

    def test_FEAT_002_3_assert_consistent_leve_si_incoherent(
        self, tmp_path: Path
    ) -> None:
        db_file = tmp_path / "empty.db"
        settings = AuthDatabaseSettings(
            database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
        )
        migrator = AuthDatabaseMigrator(settings)
        engine = migrator.create_engine()
        try:
            with pytest.raises(AssertionError, match="Incohérence migration"):
                MigrationOrmConsistencyChecker().assert_consistent(engine)
        finally:
            engine.dispose()

    def test_FEAT_002_3_detecte_colonne_manquante(self, tmp_path: Path) -> None:
        db_file = tmp_path / "partial.db"
        settings = AuthDatabaseSettings(
            database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
        )
        migrator = AuthDatabaseMigrator(settings)
        migrator.upgrade_head()
        engine = migrator.create_engine()
        try:
            with engine.begin() as conn:
                conn.execute(text("DROP TABLE auth_users"))
                conn.execute(
                    text(
                        "CREATE TABLE auth_users ("
                        "id VARCHAR(64) PRIMARY KEY, auth_subject VARCHAR(255))"
                    )
                )
            mismatches = MigrationOrmConsistencyChecker().check(engine)
            assert any(
                m.table == "auth_users" and m.detail.startswith("Colonne ORM")
                for m in mismatches
            )
        finally:
            engine.dispose()

    def test_FEAT_002_3_detecte_table_manquante(self, tmp_path: Path) -> None:
        db_file = tmp_path / "bare.db"
        settings = AuthDatabaseSettings(
            database_url=SecretStr(f"sqlite:///{db_file.as_posix()}"),
        )
        migrator = AuthDatabaseMigrator(settings)
        engine = migrator.create_engine()
        try:
            mismatches = MigrationOrmConsistencyChecker().check(engine)
            assert any(m.column == "*" for m in mismatches)
            assert isinstance(mismatches[0], MigrationOrmMismatch)
        finally:
            engine.dispose()
