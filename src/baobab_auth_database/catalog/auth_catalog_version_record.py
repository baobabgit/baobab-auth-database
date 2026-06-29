"""Enregistrement de version catalogue appliquée.

:spec: FEAT-006.4
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AuthCatalogVersionRecord:
    """Trace d'une application réussie du catalogue RBAC.

    :spec: FEAT-006.4
    """

    id: str
    core_version: str
    compat_profile: str
    catalog_checksum: str
    applied_at: datetime
    applied_by: str | None = None
    metadata_json: str | None = None
