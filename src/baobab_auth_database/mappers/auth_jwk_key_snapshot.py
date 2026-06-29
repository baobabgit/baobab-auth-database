"""Snapshot de persistance clé JWK (pas d'entité core en v0.5.1).

:spec: FEAT-004.1
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AuthJwkKeySnapshot:
    """Données JWK persistées — DTO interne à la couche database.

    :param id: Identifiant interne.
    :param kid: Key ID public (JWT header).
    :param algorithm: Algorithme (ex. RS256).
    :param public_key: Clé publique sérialisée.
    :param private_key_encrypted: Clé privée chiffrée.
    :param is_active: Indique si la clé est active.
    :param created_at: Date de création (UTC).
    :param expires_at: Date d'expiration optionnelle (UTC).
    :param revoked_at: Date de révocation optionnelle (UTC).
    :spec: FEAT-004.1
    """

    id: str
    kid: str
    algorithm: str
    public_key: str
    private_key_encrypted: str
    is_active: bool
    created_at: datetime
    expires_at: datetime | None
    revoked_at: datetime | None
