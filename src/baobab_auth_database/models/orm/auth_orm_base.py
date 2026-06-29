"""Base ORM SQLAlchemy pour les modèles auth.

:spec: FEAT-002.1
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)


class AuthOrmBase(DeclarativeBase):
    """Classe de base déclarative avec convention de nommage des contraintes.

    :spec: FEAT-002.1
    """

    metadata = MetaData(
        naming_convention=AuthTableNamingConvention.metadata_naming_convention(),
    )
