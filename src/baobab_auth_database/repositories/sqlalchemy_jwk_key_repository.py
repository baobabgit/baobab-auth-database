"""Repository SQLAlchemy des clés JWK.

:spec: FEAT-003.1
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from baobab_auth_database.mappers.auth_jwk_key_orm_mapper import AuthJwkKeyOrmMapper
from baobab_auth_database.mappers.auth_jwk_key_snapshot import AuthJwkKeySnapshot
from baobab_auth_database.models.orm.auth_jwk_key_model import AuthJwkKeyModel
from baobab_auth_database.repositories.sqlalchemy_persistence_guard import (
    SqlAlchemyPersistenceGuard,
)


class SqlAlchemyJwkKeyRepository:
    """Persistance des clés JWK (snapshot local — pas de port core en v0.5.1).

    :spec: FEAT-003.1
    """

    def __init__(
        self,
        session: Session,
        mapper: AuthJwkKeyOrmMapper | None = None,
    ) -> None:
        """Injecte la session et le mapper.

        :param session: Session SQLAlchemy partagée.
        :param mapper: Mapper JWK ; instance par défaut si omis.
        """
        self._session = session
        self._mapper = mapper or AuthJwkKeyOrmMapper()

    def get_by_id(self, key_id: str) -> AuthJwkKeySnapshot | None:
        """Récupère une clé par identifiant interne.

        :param key_id: Identifiant persisté.
        :returns: Snapshot ou ``None``.
        """
        model = self._session.get(AuthJwkKeyModel, key_id)
        if model is None:
            return None
        return self._mapper.to_snapshot(model)

    def get_by_kid(self, kid: str) -> AuthJwkKeySnapshot | None:
        """Récupère une clé par ``kid`` JWT.

        :param kid: Key ID public.
        :returns: Snapshot ou ``None``.
        """
        model = self._session.scalars(
            select(AuthJwkKeyModel).where(AuthJwkKeyModel.kid == kid)
        ).first()
        if model is None:
            return None
        return self._mapper.to_snapshot(model)

    def save(self, snapshot: AuthJwkKeySnapshot) -> None:
        """Crée ou met à jour une clé JWK.

        :param snapshot: Données persistables.
        """
        self._session.merge(self._mapper.to_model(snapshot))
        SqlAlchemyPersistenceGuard.flush(self._session)

    def list_active(self) -> tuple[AuthJwkKeySnapshot, ...]:
        """Liste les clés actives.

        :returns: Snapshots triés par ``kid``.
        """
        models = self._session.scalars(
            select(AuthJwkKeyModel)
            .where(AuthJwkKeyModel.is_active.is_(True))
            .order_by(AuthJwkKeyModel.kid)
        ).all()
        return tuple(self._mapper.to_snapshot(model) for model in models)
