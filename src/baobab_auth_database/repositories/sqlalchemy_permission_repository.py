"""Repository SQLAlchemy des permissions.

:spec: FEAT-003.1
"""

from baobab_auth_core.domain.entities.permission import Permission
from baobab_auth_core.domain.value_objects.permission_id import PermissionId
from baobab_auth_core.domain.value_objects.permission_name import PermissionName
from sqlalchemy import select
from sqlalchemy.orm import Session

from baobab_auth_database.mappers.auth_permission_orm_mapper import (
    AuthPermissionOrmMapper,
)
from baobab_auth_database.models.orm.auth_permission_model import AuthPermissionModel
from baobab_auth_database.repositories.sqlalchemy_persistence_guard import (
    SqlAlchemyPersistenceGuard,
)


class SqlAlchemyPermissionRepository:
    """Implémentation synchrone du port ``PermissionRepository``.

    :spec: FEAT-003.1
    """

    def __init__(
        self,
        session: Session,
        mapper: AuthPermissionOrmMapper | None = None,
    ) -> None:
        """Injecte la session et le mapper.

        :param session: Session SQLAlchemy partagée.
        :param mapper: Mapper permission ; instance par défaut si omis.
        """
        self._session = session
        self._mapper = mapper or AuthPermissionOrmMapper()

    def get_by_id(self, permission_id: PermissionId) -> Permission | None:
        """Récupère une permission par identifiant.

        :param permission_id: Identifiant core.
        :returns: Entité ou ``None``.
        """
        model = self._session.get(AuthPermissionModel, str(permission_id))
        if model is None:
            return None
        return self._mapper.to_domain(model)

    def get_by_name(self, name: PermissionName) -> Permission | None:
        """Récupère une permission par nom.

        :param name: Nom canonique.
        :returns: Entité ou ``None``.
        """
        model = self._session.scalars(
            select(AuthPermissionModel).where(AuthPermissionModel.name == str(name))
        ).first()
        if model is None:
            return None
        return self._mapper.to_domain(model)

    def save(self, permission: Permission) -> None:
        """Crée ou met à jour une permission.

        :param permission: Entité core.
        """
        self._session.merge(self._mapper.to_model(permission))
        SqlAlchemyPersistenceGuard.flush(self._session)

    def list_all(self) -> list[Permission]:
        """Liste toutes les permissions.

        :returns: Liste des permissions.
        """
        return list(self.list_permissions())

    def list_permissions(self) -> tuple[Permission, ...]:
        """Liste toutes les permissions.

        :returns: Tuple des permissions.
        """
        models = self._session.scalars(
            select(AuthPermissionModel).order_by(AuthPermissionModel.name)
        ).all()
        return tuple(self._mapper.to_domain(model) for model in models)
