"""Diagnostics read-only du catalogue RBAC en base.

:spec: FEAT-006.3
"""

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog
from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.entities.role import Role
from sqlalchemy.orm import Session

from baobab_auth_database.catalog.auth_catalog_checksum import AuthCatalogChecksum
from baobab_auth_database.catalog.auth_catalog_compat_profile import (
    AuthCatalogCompatProfile,
)
from baobab_auth_database.catalog.auth_catalog_diagnostic_report import (
    AuthCatalogDiagnosticReport,
)
from baobab_auth_database.repositories.sqlalchemy_permission_repository import (
    SqlAlchemyPermissionRepository,
)
from baobab_auth_database.repositories.sqlalchemy_role_repository import (
    SqlAlchemyRoleRepository,
)


class AuthCatalogDiagnostics:
    """Compare la base au catalogue core sans modification.

    :param session: Session SQLAlchemy read-only.
    :param catalog: Catalogue core injectable.
    :param compat_profile: Profil de compatibilité validé.
    :spec: FEAT-006.3
    """

    def __init__(
        self,
        session: Session,
        catalog: DefaultAuthCatalog | None = None,
        compat_profile: str | None = None,
    ) -> None:
        """Initialise le diagnostic.

        :param session: Session SQLAlchemy.
        :param catalog: Catalogue ; ``DefaultAuthCatalog`` si omis.
        :param compat_profile: Profil ; défaut ``core_051``.
        """
        self._session = session
        self._catalog = catalog or DefaultAuthCatalog()
        self._compat_profile = compat_profile or AuthCatalogCompatProfile.default()
        self._permissions = SqlAlchemyPermissionRepository(session)
        self._roles = SqlAlchemyRoleRepository(session)
        self._checksum = AuthCatalogChecksum(self._catalog)

    def run(self) -> AuthCatalogDiagnosticReport:
        """Exécute la comparaison catalogue attendu vs base.

        :returns: Rapport de diagnostic structuré.
        """
        expected_permission_names = {
            str(permission.name) for permission in self._catalog.permissions()
        }
        expected_role_names = {str(role.name) for role in self._catalog.roles()}
        expected_mappings = {
            str(role_name): tuple(sorted(str(name) for name in permission_names))
            for role_name, permission_names in self._catalog.role_permissions().items()
        }

        db_permissions = self._permissions.list_permissions()
        db_roles = self._roles.list_roles()
        db_permission_names = {str(permission.name) for permission in db_permissions}
        db_role_names = {str(role.name) for role in db_roles}

        missing_permissions = tuple(
            sorted(expected_permission_names - db_permission_names)
        )
        obsolete_permissions = tuple(
            sorted(db_permission_names - expected_permission_names)
        )
        missing_roles = tuple(sorted(expected_role_names - db_role_names))
        obsolete_roles = tuple(sorted(db_role_names - expected_role_names))

        divergent_mappings: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = []
        for role in db_roles:
            role_name = str(role.name)
            if role_name not in expected_mappings:
                continue
            expected = expected_mappings[role_name]
            actual = tuple(sorted(str(name) for name in role.permission_names))
            if actual != expected:
                divergent_mappings.append((role_name, expected, actual))

        actual_checksum = self._checksum_from_db(
            db_permissions=db_permissions,
            db_roles=db_roles,
        )

        return AuthCatalogDiagnosticReport(
            compat_profile=self._compat_profile,
            core_version=AuthCatalogCompatProfile.installed_core_version(),
            expected_checksum=self._checksum.compute(),
            actual_checksum=actual_checksum,
            missing_permissions=missing_permissions,
            obsolete_permissions=obsolete_permissions,
            missing_roles=missing_roles,
            obsolete_roles=obsolete_roles,
            divergent_role_mappings=tuple(sorted(divergent_mappings)),
        )

    def _checksum_from_db(
        self,
        *,
        db_permissions: tuple[Permission, ...],
        db_roles: tuple[Role, ...],
    ) -> str:
        """Calcule un checksum à partir des données persistées.

        :param db_permissions: Permissions en base.
        :param db_roles: Rôles en base.
        :returns: Empreinte hex ou chaîne vide si base vide.
        """
        if not db_permissions and not db_roles:
            return ""
        parts: list[str] = []
        for permission in db_permissions:
            parts.append(
                "|".join(
                    (
                        "permission",
                        str(permission.name),
                        permission.resource,
                        permission.action,
                        permission.description or "",
                    )
                )
            )
        for role in db_roles:
            permission_names = ",".join(
                sorted(str(name) for name in role.permission_names)
            )
            parts.append(
                "|".join(
                    (
                        "role",
                        str(role.name),
                        role.description or "",
                        permission_names,
                    )
                )
            )
        parts.sort()
        return AuthCatalogChecksum.hash_parts(parts)
