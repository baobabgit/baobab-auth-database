"""Vérification de cohérence schéma migré ↔ modèles ORM.

:spec: FEAT-002.3
"""

from dataclasses import dataclass

from sqlalchemy import inspect
from sqlalchemy.engine import Engine

from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase
from baobab_auth_database.models.orm.auth_orm_registry import AuthOrmRegistry


@dataclass(frozen=True)
class MigrationOrmMismatch:
    """Écart détecté entre le schéma migré et un modèle ORM.

    :param table: Nom de la table concernée.
    :param column: Nom de la colonne manquante ou en trop.
    :param detail: Description de l'écart.
    """

    table: str
    column: str
    detail: str


class MigrationOrmConsistencyChecker:
    """Compare les colonnes ORM aux colonnes du schéma réellement migré.

    :spec: FEAT-002.3
    """

    def check(self, engine: Engine) -> tuple[MigrationOrmMismatch, ...]:
        """Inspecte la base et signale les colonnes ORM absentes du schéma.

        :param engine: Engine connecté à une base migrée jusqu'à ``head``.
        :returns: Tuple des écarts détectés (vide si cohérent).
        """
        inspector = inspect(engine)
        mismatches: list[MigrationOrmMismatch] = []

        for model in AuthOrmRegistry.MODELS:
            table_name = model.__tablename__
            if table_name not in inspector.get_table_names():
                mismatches.append(
                    MigrationOrmMismatch(
                        table=table_name,
                        column="*",
                        detail="Table absente du schéma migré.",
                    )
                )
                continue

            db_columns = {col["name"] for col in inspector.get_columns(table_name)}
            orm_columns = {col.name for col in model.__table__.columns}

            for missing in sorted(orm_columns - db_columns):
                mismatches.append(
                    MigrationOrmMismatch(
                        table=table_name,
                        column=missing,
                        detail="Colonne ORM absente du schéma migré.",
                    )
                )

        return tuple(mismatches)

    def assert_consistent(self, engine: Engine) -> None:
        """Lève ``AssertionError`` si le schéma migré diverge des modèles ORM.

        :param engine: Engine connecté à une base migrée.
        :raises AssertionError: Si au moins un écart est détecté.
        """
        mismatches = self.check(engine)
        if mismatches:
            lines = "\n".join(
                f"  - {m.table}.{m.column}: {m.detail}" for m in mismatches
            )
            msg = f"Incohérence migration ↔ ORM :\n{lines}"
            raise AssertionError(msg)

        if not AuthOrmBase.metadata.tables:
            msg = "Métadonnées ORM vides."
            raise AssertionError(msg)
