"""Convention de nommage des tables auth."""

from typing import ClassVar


class AuthTableNamingConvention:
    """Centralise le préfixe et la convention de nommage des tables ORM.

    Toutes les tables auth portent le préfixe ``auth_``.

    :spec: FEAT-001.2
    """

    TABLE_PREFIX: ClassVar[str] = "auth_"

    @classmethod
    def table_name(cls, entity: str) -> str:
        """Construit le nom de table pour une entité.

        :param entity: Nom logique de l'entité (ex. ``users``).
        :returns: Nom de table SQL (ex. ``auth_users``).
        """
        normalized = entity.strip().lower()
        if normalized.startswith(cls.TABLE_PREFIX):
            return normalized
        return f"{cls.TABLE_PREFIX}{normalized}"

    @classmethod
    def metadata_naming_convention(cls) -> dict[str, str]:
        """Retourne la convention Alembic/SQLAlchemy pour ``MetaData``.

        :returns: Dictionnaire de conventions de contraintes.
        """
        return {
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
