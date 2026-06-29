"""Tests AuthCatalogChecksum."""

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog

from baobab_auth_database.catalog.auth_catalog_checksum import AuthCatalogChecksum


class TestAuthCatalogChecksum:
    """Tests FEAT-006.2 — checksum déterministe."""

    def test_FEAT_006_2_checksum_is_deterministic(self) -> None:
        catalog = DefaultAuthCatalog()
        first = AuthCatalogChecksum(catalog).compute()
        second = AuthCatalogChecksum(catalog).compute()
        assert first == second
        assert len(first) == 64

    def test_FEAT_006_2_checksum_changes_when_catalog_changes(self) -> None:
        catalog_a = DefaultAuthCatalog()
        checksum_a = AuthCatalogChecksum(catalog_a).compute()

        class _OtherCatalog(DefaultAuthCatalog):
            def permissions(self):
                perms = super().permissions()
                return perms[:1]

        checksum_b = AuthCatalogChecksum(_OtherCatalog()).compute()
        assert checksum_a != checksum_b
