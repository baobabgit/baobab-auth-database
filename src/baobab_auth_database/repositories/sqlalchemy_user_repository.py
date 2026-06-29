"""Repository SQLAlchemy des utilisateurs.

:spec: FEAT-003.1
"""

from baobab_auth_core.domain.entities.user import User
from baobab_auth_core.domain.value_objects.auth_subject import AuthSubject
from baobab_auth_core.domain.value_objects.email import Email
from baobab_auth_core.domain.value_objects.role_name import RoleName
from baobab_auth_core.domain.value_objects.user_id import UserId
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from baobab_auth_database.mappers.auth_user_orm_mapper import AuthUserOrmMapper
from baobab_auth_database.models.orm.auth_role_model import AuthRoleModel
from baobab_auth_database.models.orm.auth_user_model import AuthUserModel
from baobab_auth_database.models.orm.auth_user_role_model import AuthUserRoleModel
from baobab_auth_database.repositories.sqlalchemy_persistence_guard import (
    SqlAlchemyPersistenceGuard,
)


class SqlAlchemyUserRepository:
    """Implémentation synchrone du port ``UserRepository``.

    :spec: FEAT-003.1
    """

    def __init__(
        self, session: Session, mapper: AuthUserOrmMapper | None = None
    ) -> None:
        """Injecte la session et le mapper ORM.

        :param session: Session SQLAlchemy partagée (UoW).
        :param mapper: Mapper utilisateur ; instance par défaut si omis.
        """
        self._session = session
        self._mapper = mapper or AuthUserOrmMapper()

    def get_by_id(self, user_id: UserId) -> User | None:
        """Récupère un utilisateur par identifiant.

        :param user_id: Identifiant core.
        :returns: Entité ou ``None``.
        """
        model = self._session.get(AuthUserModel, str(user_id))
        if model is None:
            return None
        role_names = self._load_role_names(str(user_id))
        return self._mapper.to_domain(model, role_names=role_names)

    def get_by_email(self, email: Email) -> User | None:
        """Récupère un utilisateur par email normalisé.

        :param email: Email core.
        :returns: Entité ou ``None``.
        """
        stmt = select(AuthUserModel).where(AuthUserModel.normalized_email == str(email))
        model = self._session.scalars(stmt).first()
        if model is None:
            return None
        role_names = self._load_role_names(model.id)
        return self._mapper.to_domain(model, role_names=role_names)

    def get_by_auth_subject(self, auth_subject: AuthSubject) -> User | None:
        """Récupère un utilisateur par sujet d'authentification.

        :param auth_subject: Sujet stable.
        :returns: Entité ou ``None``.
        """
        stmt = select(AuthUserModel).where(
            AuthUserModel.auth_subject == str(auth_subject)
        )
        model = self._session.scalars(stmt).first()
        if model is None:
            return None
        role_names = self._load_role_names(model.id)
        return self._mapper.to_domain(model, role_names=role_names)

    def save(self, user: User) -> None:
        """Crée ou met à jour un utilisateur et ses rôles associés.

        :param user: Entité core à persister.
        """
        model = self._mapper.to_model(user)
        self._session.merge(model)
        self._sync_roles(str(user.id), user.role_names)
        SqlAlchemyPersistenceGuard.flush(self._session)

    def delete(self, user_id: UserId) -> None:
        """Supprime un utilisateur et ses associations de rôles.

        :param user_id: Identifiant à supprimer.
        """
        uid = str(user_id)
        self._session.execute(
            delete(AuthUserRoleModel).where(AuthUserRoleModel.user_id == uid)
        )
        model = self._session.get(AuthUserModel, uid)
        if model is not None:
            self._session.delete(model)
        SqlAlchemyPersistenceGuard.flush(self._session)

    def exists_by_email(self, email: Email) -> bool:
        """Indique si un utilisateur possède déjà cet email.

        :param email: Email recherché.
        :returns: ``True`` si un enregistrement existe.
        """
        stmt = select(AuthUserModel.id).where(
            AuthUserModel.normalized_email == str(email)
        )
        return self._session.scalars(stmt).first() is not None

    def _load_role_names(self, user_id: str) -> tuple[str, ...]:
        stmt = (
            select(AuthRoleModel.name)
            .join(
                AuthUserRoleModel,
                AuthUserRoleModel.role_id == AuthRoleModel.id,
            )
            .where(AuthUserRoleModel.user_id == user_id)
            .order_by(AuthRoleModel.name)
        )
        return tuple(self._session.scalars(stmt).all())

    def _sync_roles(self, user_id: str, role_names: tuple[RoleName, ...]) -> None:
        self._session.execute(
            delete(AuthUserRoleModel).where(AuthUserRoleModel.user_id == user_id)
        )
        for role_name in role_names:
            role = self._session.scalars(
                select(AuthRoleModel).where(AuthRoleModel.name == str(role_name))
            ).first()
            if role is None:
                continue
            self._session.add(AuthUserRoleModel(user_id=user_id, role_id=role.id))
