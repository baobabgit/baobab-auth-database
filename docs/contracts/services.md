# Contrat — Services publics

> Services exposés publiquement (MVP v0.1.0).

| Service | Rôle | Spec |
|---------|------|------|
| `AuthDatabaseSettings` | Configuration injectée (URL, pool) | FEAT-001.1 |
| `SqlAlchemyEngineFactory` | Création engine SQLAlchemy | FEAT-001.2 |
| `SqlAlchemySessionFactory` | Création sessions SQLAlchemy | FEAT-001.2 |
| `SqlAlchemyAuthUnitOfWork` | Unité de travail transactionnelle | FEAT-003.2 |
| `AuthCatalogBootstrap` | Seed idempotent ``DefaultAuthCatalog`` | FEAT-005.2 |
| `AuthDatabaseCli` | Migrations Alembic + bootstrap CLI | FEAT-005.1 |

Les repositories sont accessibles via les propriétés de l'UoW (``users``,
``roles``, etc.) mais leurs classes concrètes ne font pas partie du contrat public.
