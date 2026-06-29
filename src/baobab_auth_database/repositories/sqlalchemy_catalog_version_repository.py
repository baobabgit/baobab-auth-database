"""Repository SQLAlchemy des versions catalogue.

:spec: FEAT-006.4
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from baobab_auth_database.catalog.auth_catalog_version_record import (
    AuthCatalogVersionRecord,
)
from baobab_auth_database.models.orm.auth_catalog_version_model import (
    AuthCatalogVersionModel,
)
from baobab_auth_database.repositories.sqlalchemy_persistence_guard import (
    SqlAlchemyPersistenceGuard,
)


class SqlAlchemyCatalogVersionRepository:
    """Persiste et lit les traces ``auth_catalog_versions``.

    :spec: FEAT-006.4
    """

    def __init__(self, session: Session) -> None:
        """Injecte la session SQLAlchemy.

        :param session: Session partagée.
        """
        self._session = session

    def save(self, record: AuthCatalogVersionRecord) -> None:
        """Enregistre une version catalogue appliquée.

        :param record: Trace à persister.
        """
        self._session.add(
            AuthCatalogVersionModel(
                id=record.id,
                core_version=record.core_version,
                compat_profile=record.compat_profile,
                catalog_checksum=record.catalog_checksum,
                applied_at=record.applied_at,
                applied_by=record.applied_by,
                metadata_json=record.metadata_json,
            )
        )
        SqlAlchemyPersistenceGuard.flush(self._session)

    def get_latest(self) -> AuthCatalogVersionRecord | None:
        """Retourne la dernière version catalogue enregistrée.

        :returns: Enregistrement le plus récent ou ``None``.
        """
        model = self._session.scalars(
            select(AuthCatalogVersionModel)
            .order_by(AuthCatalogVersionModel.applied_at.desc())
            .limit(1)
        ).first()
        if model is None:
            return None
        return self._to_record(model)

    def list_all(self) -> tuple[AuthCatalogVersionRecord, ...]:
        """Liste toutes les versions catalogue par date décroissante.

        :returns: Tuple des enregistrements.
        """
        models = self._session.scalars(
            select(AuthCatalogVersionModel).order_by(
                AuthCatalogVersionModel.applied_at.desc()
            )
        ).all()
        return tuple(self._to_record(model) for model in models)

    @staticmethod
    def _to_record(model: AuthCatalogVersionModel) -> AuthCatalogVersionRecord:
        return AuthCatalogVersionRecord(
            id=model.id,
            core_version=model.core_version,
            compat_profile=model.compat_profile,
            catalog_checksum=model.catalog_checksum,
            applied_at=model.applied_at,
            applied_by=model.applied_by,
            metadata_json=model.metadata_json,
        )
