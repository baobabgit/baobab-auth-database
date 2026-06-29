"""Tests unitaires convention de nommage."""

from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)


class TestAuthTableNamingConvention:
    """Tests FEAT-001.2 — convention tables auth_*."""

    def test_FEAT_001_2_table_name_ajoute_prefixe(self) -> None:
        assert AuthTableNamingConvention.table_name("users") == "auth_users"

    def test_FEAT_001_2_table_name_deja_prefixe(self) -> None:
        assert AuthTableNamingConvention.table_name("auth_roles") == "auth_roles"

    def test_FEAT_001_2_metadata_naming_convention(self) -> None:
        convention = AuthTableNamingConvention.metadata_naming_convention()
        assert "pk" in convention
        assert "fk" in convention
        assert "%(table_name)s" in convention["uq"]
