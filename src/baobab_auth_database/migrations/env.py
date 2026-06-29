"""Alembic migration environment."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from baobab_auth_database.models.orm import auth_orm_registry  # noqa: F401
from baobab_auth_database.models.orm.auth_orm_base import AuthOrmBase

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = AuthOrmBase.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    url = config.get_main_option("sqlalchemy.url")
    if url is None:
        msg = "sqlalchemy.url non configurée pour Alembic."
        raise RuntimeError(msg)

    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
