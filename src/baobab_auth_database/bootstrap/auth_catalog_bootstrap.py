"""Seed idempotent des rôles et permissions système.

:spec: FEAT-005.2, FEAT-006.4
"""

from datetime import UTC, datetime
from uuid import uuid4

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog

from baobab_auth_database.catalog.auth_catalog_checksum import AuthCatalogChecksum
from baobab_auth_database.catalog.auth_catalog_compat_profile import (
    AuthCatalogCompatProfile,
)
from baobab_auth_database.catalog.auth_catalog_seed_result import AuthCatalogSeedResult
from baobab_auth_database.catalog.auth_catalog_version_record import (
    AuthCatalogVersionRecord,
)
from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.unit_of_work.sqlalchemy_auth_unit_of_work import (
    SqlAlchemyAuthUnitOfWork,
)


class AuthCatalogBootstrap:
    """Insère et synchronise le catalogue ``DefaultAuthCatalog`` sans doublon.

    :param session_factory: Factory SQLAlchemy pour ouvrir l'UoW.
    :param catalog: Catalogue core injectable (tests) ; défaut si omis.
    :param compat_profile: Profil de compatibilité validé.
    :param applied_by: Identifiant applicatif enregistré avec la version.
    :spec: FEAT-005.2, FEAT-006.4
    """

    def __init__(
        self,
        session_factory: SqlAlchemySessionFactory,
        catalog: DefaultAuthCatalog | None = None,
        compat_profile: str | None = None,
        applied_by: str | None = None,
    ) -> None:
        """Initialise le bootstrap catalogue.

        :param session_factory: Factory de sessions partagée avec l'UoW.
        :param catalog: Instance ``DefaultAuthCatalog`` ; créée si omise.
        :param compat_profile: Profil ; ``core_051`` par défaut.
        :param applied_by: Acteur du seed ; ``baobab-auth-db`` par défaut.
        """
        self._session_factory = session_factory
        self._catalog = catalog or DefaultAuthCatalog()
        self._compat_profile = compat_profile or AuthCatalogCompatProfile.default()
        self._applied_by = applied_by or "baobab-auth-db"

    def run(self, *, dry_run: bool = False) -> AuthCatalogSeedResult:
        """Persiste ou simule permissions, rôles et version catalogue.

        :param dry_run: Si ``True``, aucune écriture ni commit.
        :returns: Résumé des opérations effectuées ou simulées.
        :raises AuthDatabasePersistenceError: En cas de violation d'intégrité.
        """
        permissions_added = 0
        roles_added = 0
        roles_resynced = 0

        with SqlAlchemyAuthUnitOfWork(self._session_factory) as uow:
            for permission in self._catalog.permissions():
                if uow.permissions.get_by_name(permission.name) is None:
                    permissions_added += 1
                    if not dry_run:
                        uow.permissions.save(permission)

            for role in self._catalog.roles():
                existing = uow.roles.get_by_name(role.name)
                if existing is None:
                    roles_added += 1
                    if not dry_run:
                        uow.roles.save(role)
                    continue
                expected = tuple(sorted(str(name) for name in role.permission_names))
                actual = tuple(sorted(str(name) for name in existing.permission_names))
                if actual != expected and role.is_system:
                    roles_resynced += 1
                    if not dry_run:
                        uow.roles.save(role)

            version_recorded = False
            if not dry_run:
                checksum = AuthCatalogChecksum(self._catalog).compute()
                uow.catalog_versions.save(
                    AuthCatalogVersionRecord(
                        id=str(uuid4()),
                        core_version=AuthCatalogCompatProfile.installed_core_version(),
                        compat_profile=self._compat_profile,
                        catalog_checksum=checksum,
                        applied_at=datetime.now(tz=UTC),
                        applied_by=self._applied_by,
                    )
                )
                version_recorded = True
                uow.commit()

        return AuthCatalogSeedResult(
            permissions_added=permissions_added,
            roles_added=roles_added,
            roles_resynced=roles_resynced,
            dry_run=dry_run,
            version_recorded=version_recorded,
        )
