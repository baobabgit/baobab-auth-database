"""Contrat — symboles exportés dans ``__all__``.

:spec: FEAT-006.1
"""

import baobab_auth_database as database_pkg


class TestPublicApiContract:
    """Vérifie le contrat public du package."""

    def test_FEAT_006_1_all_symbols_are_importable(self) -> None:
        """Chaque symbole de ``__all__`` est accessible depuis le package racine."""
        for name in database_pkg.__all__:
            assert hasattr(database_pkg, name), f"missing export: {name}"

    def test_FEAT_006_1_expected_public_surface(self) -> None:
        """Surface publique MVP v0.1.0 documentée."""
        expected = {
            "AuthCatalogBootstrap",
            "AuthDatabaseCli",
            "AuthDatabaseMappingError",
            "AuthDatabasePersistenceError",
            "AuthDatabaseSettings",
            "AuthOrmValueConverter",
            "AuthTableNamingConvention",
            "SqlAlchemyAuthUnitOfWork",
            "SqlAlchemyEngineFactory",
            "SqlAlchemySessionFactory",
        }
        assert set(database_pkg.__all__) == expected
