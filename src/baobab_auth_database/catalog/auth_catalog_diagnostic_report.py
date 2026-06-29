"""Rapport de diagnostic catalogue RBAC.

:spec: FEAT-006.3
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AuthCatalogDiagnosticReport:
    """Résultat read-only d'une comparaison base vs catalogue core.

    :spec: FEAT-006.3
    """

    compat_profile: str
    core_version: str
    expected_checksum: str
    actual_checksum: str
    missing_permissions: tuple[str, ...] = field(default_factory=tuple)
    obsolete_permissions: tuple[str, ...] = field(default_factory=tuple)
    missing_roles: tuple[str, ...] = field(default_factory=tuple)
    obsolete_roles: tuple[str, ...] = field(default_factory=tuple)
    divergent_role_mappings: tuple[
        tuple[str, tuple[str, ...], tuple[str, ...]], ...
    ] = field(default_factory=tuple)

    @property
    def is_conform(self) -> bool:
        """Indique si la base correspond au catalogue attendu.

        :returns: ``True`` si aucune divergence détectée.
        """
        return (
            not self.missing_permissions
            and not self.obsolete_permissions
            and not self.missing_roles
            and not self.obsolete_roles
            and not self.divergent_role_mappings
            and self.actual_checksum == self.expected_checksum
        )

    def to_dict(self) -> dict[str, Any]:
        """Sérialise le rapport en dictionnaire JSON-compatible.

        :returns: Structure sérialisable.
        """
        return {
            "compat_profile": self.compat_profile,
            "core_version": self.core_version,
            "expected_checksum": self.expected_checksum,
            "actual_checksum": self.actual_checksum,
            "conform": self.is_conform,
            "missing_permissions": list(self.missing_permissions),
            "obsolete_permissions": list(self.obsolete_permissions),
            "missing_roles": list(self.missing_roles),
            "obsolete_roles": list(self.obsolete_roles),
            "divergent_role_mappings": [
                {
                    "role": role,
                    "expected": list(expected),
                    "actual": list(actual),
                }
                for role, expected, actual in self.divergent_role_mappings
            ],
        }
