"""Checksum déterministe du catalogue RBAC core.

:spec: FEAT-006.2
"""

import hashlib

from baobab_auth_core.domain.catalogs.default_auth_catalog import DefaultAuthCatalog


class AuthCatalogChecksum:
    """Calcule un empreinte stable du catalogue ``DefaultAuthCatalog``.

    :param catalog: Catalogue core injectable (tests).
    :spec: FEAT-006.2
    """

    def __init__(self, catalog: DefaultAuthCatalog | None = None) -> None:
        """Initialise le calculateur.

        :param catalog: Catalogue ; ``DefaultAuthCatalog`` si omis.
        """
        self._catalog = catalog or DefaultAuthCatalog()

    def compute(self) -> str:
        """Calcule le checksum SHA-256 hex du catalogue.

        :returns: Empreinte hexadécimale sur 64 caractères.
        """
        parts: list[str] = []
        for permission in self._catalog.permissions():
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
        for role in self._catalog.roles():
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
        return self.hash_parts(parts)

    @staticmethod
    def hash_parts(parts: list[str]) -> str:
        """Hash une liste de segments triés.

        :param parts: Segments canoniques du catalogue.
        :returns: Empreinte SHA-256 hex.
        """
        payload = "\n".join(parts)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()
