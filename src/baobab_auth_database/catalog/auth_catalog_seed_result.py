"""Résultat d'une opération de seed catalogue.

:spec: FEAT-006.4
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthCatalogSeedResult:
    """Résumé d'un seed catalogue (réel ou dry-run).

    :spec: FEAT-006.4
    """

    permissions_added: int
    roles_added: int
    roles_resynced: int
    dry_run: bool
    version_recorded: bool

    @property
    def changed(self) -> bool:
        """Indique si le seed aurait modifié ou a modifié la base.

        :returns: ``True`` si au moins une mutation catalogue.
        """
        return (
            self.permissions_added > 0
            or self.roles_added > 0
            or self.roles_resynced > 0
        )
