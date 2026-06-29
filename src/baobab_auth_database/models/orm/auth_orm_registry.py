"""Registre des modèles ORM auth pour création de schéma.

:spec: FEAT-002.1
"""

from sqlalchemy.engine import Engine

from baobab_auth_database.models.orm.auth_audit_event_model import AuthAuditEventModel
from baobab_auth_database.models.orm.auth_jwk_key_model import AuthJwkKeyModel
from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.models.orm.auth_permission_model import AuthPermissionModel
from baobab_auth_database.models.orm.auth_role_model import AuthRoleModel
from baobab_auth_database.models.orm.auth_role_permission_model import (
    AuthRolePermissionModel,
)
from baobab_auth_database.models.orm.auth_session_model import AuthSessionModel
from baobab_auth_database.models.orm.auth_user_model import AuthUserModel
from baobab_auth_database.models.orm.auth_user_profile_model import AuthUserProfileModel
from baobab_auth_database.models.orm.auth_user_role_model import AuthUserRoleModel


class AuthOrmRegistry:
    """Expose les modèles ORM et permet de créer le schéma.

    :spec: FEAT-002.1
    """

    MODELS: tuple[type[AuthOrmBase], ...] = (
        AuthUserModel,
        AuthUserProfileModel,
        AuthRoleModel,
        AuthPermissionModel,
        AuthUserRoleModel,
        AuthRolePermissionModel,
        AuthSessionModel,
        AuthAuditEventModel,
        AuthJwkKeyModel,
    )

    @classmethod
    def create_all(cls, engine: Engine) -> None:
        """Crée toutes les tables auth sur l'engine fourni.

        :param engine: Engine SQLAlchemy cible.
        """
        AuthOrmBase.metadata.create_all(engine)

    @classmethod
    def drop_all(cls, engine: Engine) -> None:
        """Supprime toutes les tables auth (tests uniquement).

        :param engine: Engine SQLAlchemy cible.
        """
        AuthOrmBase.metadata.drop_all(engine)

    @classmethod
    def table_names(cls) -> tuple[str, ...]:
        """Retourne les noms de tables dans l'ordre du registre.

        :returns: Noms de tables SQL.
        """
        return tuple(model.__tablename__ for model in cls.MODELS)
