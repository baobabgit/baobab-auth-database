"""Librairie de persistance Baobab Auth."""

from baobab_auth_database.bootstrap.auth_catalog_bootstrap import AuthCatalogBootstrap
from baobab_auth_database.cli.auth_database_cli import AuthDatabaseCli
from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)
from baobab_auth_database.exceptions.persistence import AuthDatabasePersistenceError
from baobab_auth_database.factories.sqlalchemy_engine_factory import (
    SqlAlchemyEngineFactory,
)
from baobab_auth_database.factories.sqlalchemy_session_factory import (
    SqlAlchemySessionFactory,
)
from baobab_auth_database.mappers.auth_orm_value_converter import (
    AuthOrmValueConverter,
)
from baobab_auth_database.naming.auth_table_naming_convention import (
    AuthTableNamingConvention,
)
from baobab_auth_database.settings.auth_database_settings import AuthDatabaseSettings
from baobab_auth_database.unit_of_work.sqlalchemy_auth_unit_of_work import (
    SqlAlchemyAuthUnitOfWork,
)

__all__ = [
    "AuthCatalogBootstrap",
    "AuthDatabaseCli",
    "AuthDatabaseMappingError",
    "AuthDatabasePersistenceError",
    "AuthDatabaseSettings",
    "AuthOrmValueConverter",
    "AuthTableNamingConvention",
    "SqlAlchemyAuthUnitOfWork",
    "SqlAlchemyEngineFactory",
    "SqlAlchemySessionFactory",
]
