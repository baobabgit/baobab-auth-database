"""Mapper ORM clé JWK ↔ snapshot de persistance.

:spec: FEAT-004.1
"""

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.mappers.auth_jwk_key_snapshot import AuthJwkKeySnapshot
from baobab_auth_database.mappers.auth_orm_value_converter import AuthOrmValueConverter
from baobab_auth_database.models.orm.auth_jwk_key_model import AuthJwkKeyModel


class AuthJwkKeyOrmMapper:
    """Convertit ``AuthJwkKeyModel`` en :class:`AuthJwkKeySnapshot` et inversement.

    :spec: FEAT-004.1
    """

    def to_snapshot(self, model: AuthJwkKeyModel) -> AuthJwkKeySnapshot:
        """Construit un snapshot depuis le modèle ORM.

        :param model: Ligne ``auth_jwk_keys``.
        :returns: Snapshot typé.
        :raises AuthDatabaseMappingError: Si un champ obligatoire est invalide.
        """
        try:
            return AuthJwkKeySnapshot(
                id=AuthOrmValueConverter.require_non_empty(model.id, "id"),
                kid=AuthOrmValueConverter.require_non_empty(model.kid, "kid"),
                algorithm=AuthOrmValueConverter.require_non_empty(
                    model.algorithm, "algorithm"
                ),
                public_key=AuthOrmValueConverter.require_non_empty(
                    model.public_key, "public_key"
                ),
                private_key_encrypted=AuthOrmValueConverter.require_non_empty(
                    model.private_key_encrypted, "private_key_encrypted"
                ),
                is_active=model.is_active,
                created_at=model.created_at,
                expires_at=model.expires_at,
                revoked_at=model.revoked_at,
            )
        except AuthDatabaseMappingError:
            raise
        except ValueError as exc:
            msg = "Impossible de mapper AuthJwkKeyModel vers AuthJwkKeySnapshot."
            raise AuthDatabaseMappingError(msg, cause=exc) from exc

    def to_model(self, snapshot: AuthJwkKeySnapshot) -> AuthJwkKeyModel:
        """Construit un modèle ORM depuis un snapshot.

        :param snapshot: Données JWK persistables.
        :returns: Modèle SQLAlchemy.
        """
        return AuthJwkKeyModel(
            id=snapshot.id,
            kid=snapshot.kid,
            algorithm=snapshot.algorithm,
            public_key=snapshot.public_key,
            private_key_encrypted=snapshot.private_key_encrypted,
            is_active=snapshot.is_active,
            created_at=snapshot.created_at,
            expires_at=snapshot.expires_at,
            revoked_at=snapshot.revoked_at,
        )
