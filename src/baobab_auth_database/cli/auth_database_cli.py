"""CLI migrations Alembic et bootstrap catalogue.

:spec: FEAT-005.1, FEAT-006.5
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING

from baobab_auth_database.bootstrap.auth_catalog_bootstrap import AuthCatalogBootstrap
from baobab_auth_database.catalog.auth_catalog_compat_profile import (
    AuthCatalogCompatProfile,
)
from baobab_auth_database.catalog.auth_catalog_diagnostic_report import (
    AuthCatalogDiagnosticReport,
)
from baobab_auth_database.catalog.auth_catalog_diagnostics import AuthCatalogDiagnostics
from baobab_auth_database.catalog.auth_catalog_report_formatter import (
    AuthCatalogReportFormatter,
)
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

    :spec: FEAT-005.1, FEAT-006.5
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
        return self._dispatch(args)

    def _dispatch(self, args: argparse.Namespace) -> int:
        """Route une sous-commande vers son handler typé.

        :param args: Arguments parsés.
        :returns: Code de sortie CLI.
        """
        if args.command == "upgrade":
            return self._cmd_upgrade(args)
        if args.command == "downgrade":
            return self._cmd_downgrade(args)
        if args.command == "current":
            return self._cmd_current(args)
        if args.command == "history":
            return self._cmd_history(args)
        if args.command == "bootstrap":
            return self._cmd_bootstrap(args)
        if args.command == "catalog":
            return self._dispatch_catalog(args)
        msg = f"Unknown command: {args.command!r}"
        raise ValueError(msg)

    def _dispatch_catalog(self, args: argparse.Namespace) -> int:
        """Route les sous-commandes ``catalog``.

        :param args: Arguments parsés avec ``catalog_command``.
        :returns: Code de sortie CLI.
        """
        if args.catalog_command == "check":
            return self._cmd_catalog_check(args)
        if args.catalog_command == "seed":
            return self._cmd_catalog_seed(args)
        if args.catalog_command == "report":
            return self._cmd_catalog_report(args)
        msg = f"Unknown catalog command: {args.catalog_command!r}"
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

        catalog_parser = subparsers.add_parser(
            "catalog",
            help="Diagnostics et synchronisation catalogue RBAC.",
        )
        catalog_sub = catalog_parser.add_subparsers(dest="catalog_command")

        check_parser = catalog_sub.add_parser(
            "check",
            help="Vérifie la conformité catalogue sans modifier la base.",
        )
        self._add_catalog_options(check_parser)

        seed_parser = catalog_sub.add_parser(
            "seed",
            help="Synchronise le catalogue core (non destructif).",
        )
        self._add_catalog_options(seed_parser)
        seed_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simule le seed sans écrire en base.",
        )

        report_parser = catalog_sub.add_parser(
            "report",
            help="Produit un rapport de diagnostic catalogue.",
        )
        self._add_catalog_options(report_parser)

        return parser

    @staticmethod
    def _add_catalog_options(parser: argparse.ArgumentParser) -> None:
        """Ajoute les options communes aux commandes catalogue.

        :param parser: Sous-parseur catalogue à enrichir.
        """
        parser.add_argument(
            "--profile",
            default=AuthCatalogCompatProfile.default(),
            help="Profil de compatibilité (défaut: core_051).",
        )
        parser.add_argument(
            "--format",
            choices=("text", "json"),
            default="text",
            help="Format de sortie pour check et report.",
        )

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

    def _cmd_catalog_check(self, args: argparse.Namespace) -> int:
        """Vérifie la conformité catalogue.

        :param args: Arguments CLI catalogue check.
        :returns: 0 si conforme, 1 si divergent.
        """
        report = self._run_catalog_diagnostics(args.profile)
        self._print_report(report, args.format)
        return 0 if report.is_conform else 1

    def _cmd_catalog_report(self, args: argparse.Namespace) -> int:
        """Affiche un rapport catalogue.

        :param args: Arguments CLI catalogue report.
        :returns: 0 si succès.
        """
        report = self._run_catalog_diagnostics(args.profile)
        self._print_report(report, args.format)
        return 0

    def _cmd_catalog_seed(self, args: argparse.Namespace) -> int:
        """Synchronise le catalogue core.

        :param args: Arguments CLI catalogue seed.
        :returns: 0 si succès.
        """
        profile = AuthCatalogCompatProfile.validate(args.profile)
        session_factory = SqlAlchemySessionFactory(self._settings)
        bootstrap = AuthCatalogBootstrap(
            session_factory,
            compat_profile=profile,
        )
        result = bootstrap.run(dry_run=args.dry_run)
        if args.format == "json":
            print(
                json.dumps(
                    {
                        "dry_run": result.dry_run,
                        "permissions_added": result.permissions_added,
                        "roles_added": result.roles_added,
                        "roles_resynced": result.roles_resynced,
                        "version_recorded": result.version_recorded,
                    },
                    sort_keys=True,
                )
            )
        else:
            mode = "dry-run" if result.dry_run else "applied"
            print(
                f"catalog seed ({mode}): "
                f"permissions={result.permissions_added}, "
                f"roles={result.roles_added}, "
                f"resynced={result.roles_resynced}, "
                f"version_recorded={result.version_recorded}"
            )
        return 0

    def _run_catalog_diagnostics(self, profile: str) -> AuthCatalogDiagnosticReport:
        """Exécute les diagnostics catalogue sur la base configurée.

        :param profile: Profil de compatibilité demandé.
        :returns: Rapport de diagnostic.
        """
        validated = AuthCatalogCompatProfile.validate(profile)
        session_factory = SqlAlchemySessionFactory(self._settings)
        session = session_factory.create()
        try:
            return AuthCatalogDiagnostics(
                session,
                compat_profile=validated,
            ).run()
        finally:
            session.close()

    @staticmethod
    def _print_report(report: AuthCatalogDiagnosticReport, output_format: str) -> None:
        """Affiche un rapport texte ou JSON.

        :param report: Rapport de diagnostic.
        :param output_format: ``text`` ou ``json``.
        """
        if output_format == "json":
            print(json.dumps(report.to_dict(), sort_keys=True))
            return
        print(AuthCatalogReportFormatter().format(report))

    def _default_bootstrap_factory(
        self, settings: AuthDatabaseSettings
    ) -> AuthCatalogBootstrap:
        """Construit le bootstrap par défaut depuis les settings.

        :param settings: Configuration injectée.
        :returns: Instance ``AuthCatalogBootstrap``.
        """
        session_factory = SqlAlchemySessionFactory(settings)
        return AuthCatalogBootstrap(session_factory)
