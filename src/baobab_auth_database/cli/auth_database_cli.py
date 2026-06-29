"""CLI migrations Alembic et bootstrap catalogue.

:spec: FEAT-005.1
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

from baobab_auth_database.bootstrap.auth_catalog_bootstrap import AuthCatalogBootstrap
from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.migrations.auth_database_migrator import AuthDatabaseMigrator
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings

if TYPE_CHECKING:
    from baobab_auth_database.bootstrap.auth_catalog_bootstrap import (
        AuthCatalogBootstrap as AuthCatalogBootstrapType,
    )
    from baobab_auth_database.migrations.auth_database_migrator import (
        AuthDatabaseMigrator as AuthDatabaseMigratorType,
    )


class AuthDatabaseCli:
    """Point d'entrée CLI pour migrations et bootstrap catalogue.

    :spec: FEAT-005.1
    """

    def __init__(
        self,
        settings: AuthDatabaseSettings | None = None,
        migrator_factory: (
            Callable[[AuthDatabaseSettings], AuthDatabaseMigratorType] | None
        ) = None,
        bootstrap_factory: (
            Callable[[AuthDatabaseSettings], AuthCatalogBootstrapType] | None
        ) = None,
    ) -> None:
        """Injecte la configuration et les factories testables.

        :param settings: Paramètres ; chargés depuis l'environnement si omis.
        :param migrator_factory: Factory de migrateur (tests).
        :param bootstrap_factory: Factory de bootstrap (tests).
        """
        self._settings = settings or AuthDatabaseSettings()
        self._migrator_factory = migrator_factory or (
            lambda configured: AuthDatabaseMigrator(configured)
        )
        self._bootstrap_factory = bootstrap_factory or self._default_bootstrap_factory

    @classmethod
    def main(cls) -> None:
        """Point d'entrée ``console_scripts`` ; propage le code de sortie."""
        sys.exit(cls().run())

    def run(self, argv: list[str] | None = None) -> int:
        """Parse les arguments et exécute la sous-commande demandée.

        :param argv: Arguments CLI ; ``sys.argv[1:]`` si omis.
        :returns: Code de sortie (0 = succès).
        """
        parser = self._build_parser()
        args = parser.parse_args(argv)
        if args.command is None:
            parser.print_help()
            return 1
        return self._dispatch(args.command, args)

    def _dispatch(self, command: str, args: argparse.Namespace) -> int:
        """Route une sous-commande vers son handler typé.

        :param command: Nom de la sous-commande.
        :param args: Arguments parsés.
        :returns: Code de sortie CLI.
        """
        if command == "upgrade":
            return self._cmd_upgrade(args)
        if command == "downgrade":
            return self._cmd_downgrade(args)
        if command == "current":
            return self._cmd_current(args)
        if command == "history":
            return self._cmd_history(args)
        if command == "bootstrap":
            return self._cmd_bootstrap(args)
        msg = f"Unknown command: {command!r}"
        raise ValueError(msg)

    def _build_parser(self) -> argparse.ArgumentParser:
        """Construit le parseur argparse avec les sous-commandes.

        :returns: Parseur configuré.
        """
        parser = argparse.ArgumentParser(
            prog="baobab-auth-db",
            description="Migrations Alembic et bootstrap catalogue Baobab Auth.",
        )
        subparsers = parser.add_subparsers(dest="command")

        subparsers.add_parser("upgrade", help="Applique les migrations jusqu'à head.")
        subparsers.add_parser("downgrade", help="Annule les migrations jusqu'à base.")
        subparsers.add_parser("current", help="Affiche la révision Alembic courante.")
        subparsers.add_parser("history", help="Liste les révisions Alembic.")
        subparsers.add_parser(
            "bootstrap",
            help="Seed idempotent des rôles et permissions DefaultAuthCatalog.",
        )
        return parser

    def _cmd_upgrade(self, _args: argparse.Namespace) -> int:
        """Applique ``upgrade head``.

        :returns: 0 si succès.
        """
        self._migrator_factory(self._settings).upgrade_head()
        return 0

    def _cmd_downgrade(self, _args: argparse.Namespace) -> int:
        """Applique ``downgrade base``.

        :returns: 0 si succès.
        """
        self._migrator_factory(self._settings).downgrade_base()
        return 0

    def _cmd_current(self, _args: argparse.Namespace) -> int:
        """Affiche la révision courante.

        :returns: 0 si succès.
        """
        revision = self._migrator_factory(self._settings).current_revision()
        print(revision if revision is not None else "base")
        return 0

    def _cmd_history(self, _args: argparse.Namespace) -> int:
        """Affiche l'historique des révisions.

        :returns: 0 si succès.
        """
        history = self._migrator_factory(self._settings).history_ids()
        for revision_id in history:
            print(revision_id)
        return 0

    def _cmd_bootstrap(self, _args: argparse.Namespace) -> int:
        """Exécute le bootstrap catalogue idempotent.

        :returns: 0 si succès.
        """
        self._bootstrap_factory(self._settings).run()
        return 0

    def _default_bootstrap_factory(
        self, settings: AuthDatabaseSettings
    ) -> AuthCatalogBootstrap:
        """Construit le bootstrap par défaut depuis les settings.

        :param settings: Configuration injectée.
        :returns: Instance ``AuthCatalogBootstrap``.
        """
        session_factory = SqlAlchemySessionFactory(settings)
        return AuthCatalogBootstrap(session_factory)
