"""Tests unitaires AuthDatabaseSettings."""

import pytest
from pydantic import SecretStr

from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings


class TestAuthDatabaseSettings:
    """Tests FEAT-001.1 — configuration persistance."""

    def test_FEAT_001_1_cas_nominal_sqlite_defaut(self) -> None:
        settings = AuthDatabaseSettings()
        assert settings.resolved_database_url().startswith("sqlite")
        assert settings.echo_sql is False
        assert settings.pool_size == 5

    def test_FEAT_001_1_cas_nominal_postgresql(self) -> None:
        settings = AuthDatabaseSettings(
            database_url=SecretStr("postgresql://user:pass@localhost/auth"),
        )
        assert settings.resolved_database_url().startswith("postgresql://")

    def test_FEAT_001_1_sqlite_avec_driver(self) -> None:
        settings = AuthDatabaseSettings(
            database_url=SecretStr("sqlite+pysqlite:///:memory:"),
        )
        assert settings.resolved_database_url().startswith("sqlite+pysqlite")

    def test_FEAT_001_1_schema_non_supporte(self) -> None:
        with pytest.raises(ValueError, match="Schéma SQLAlchemy non supporté"):
            AuthDatabaseSettings(database_url=SecretStr("mysql://localhost/db"))

    def test_FEAT_001_1_repr_sans_secret(self) -> None:
        settings = AuthDatabaseSettings(
            database_url=SecretStr("postgresql://secret:secret@localhost/auth"),
        )
        text = repr(settings)
        assert "secret" not in text
        assert "database_url='***'" in text
