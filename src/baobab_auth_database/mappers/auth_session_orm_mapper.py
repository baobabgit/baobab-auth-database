"""Mapper ORM session ↔ entité ``Session`` du core.

:spec: FEAT-004.1
"""

from baobab_auth_core.domain.entities.session import Session
from baobab_auth_core.domain.enums.session_status import SessionStatus
from baobab_auth_core.domain.value_objects.session_id import SessionId
from baobab_auth_core.domain.value_objects.token_id import TokenId
from baobab_auth_core.domain.value_objects.user_id import UserId
from baobab_auth_core.exceptions.validation import ValidationError

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.mappers.auth_orm_value_converter import AuthOrmValueConverter
from baobab_auth_database.models.orm.auth_session_model import AuthSessionModel


class AuthSessionOrmMapper:
    """Convertit ``AuthSessionModel`` en :class:`Session` et inversement.

    La colonne ``refresh_token_hash`` stocke la valeur du ``TokenId`` core.

    :spec: FEAT-004.1
    """

    def to_domain(self, model: AuthSessionModel) -> Session:
        """Construit une entité ``Session`` depuis le modèle ORM.

        :param model: Ligne ``auth_sessions``.
        :returns: Entité core.
        :raises AuthDatabaseMappingError: Si la conversion échoue.
        """
        try:
            return Session(
                id=SessionId(model.id),
                user_id=UserId(model.user_id),
                refresh_token_id=TokenId(model.refresh_token_hash),
                status=AuthOrmValueConverter.to_enum(
                    SessionStatus, model.status, "status"
                ),
                created_at=model.created_at,
                expires_at=model.expires_at,
                revoked_at=model.revoked_at,
                last_used_at=model.last_used_at,
                user_agent=model.user_agent,
                ip_address=model.ip_address,
                device_label=model.device_label,
            )
        except (ValidationError, ValueError) as exc:
            msg = "Impossible de mapper AuthSessionModel vers Session."
            raise AuthDatabaseMappingError(msg, cause=exc) from exc

    def to_model(self, session: Session) -> AuthSessionModel:
        """Construit un modèle ORM depuis une entité ``Session``.

        :param session: Entité core.
        :returns: Modèle SQLAlchemy.
        """
        return AuthSessionModel(
            id=str(session.id),
            user_id=str(session.user_id),
            refresh_token_hash=str(session.refresh_token_id),
            status=session.status.value,
            created_at=session.created_at,
            expires_at=session.expires_at,
            revoked_at=session.revoked_at,
            last_used_at=session.last_used_at,
            user_agent=session.user_agent,
            ip_address=session.ip_address,
            device_label=session.device_label,
        )
