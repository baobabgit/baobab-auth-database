# Contrat — API publique

> Symboles exportés dans ``baobab_auth_database.__all__`` (MVP v0.1.0).
> Toute modification incompatible déclenche un bump SemVer majeur.

## Symboles exportés

| Symbole | Type | Module | Spec |
|---------|------|--------|------|
| `AuthDatabaseSettings` | Classe | `settings.auth_database_settings` | FEAT-001.1 |
| `SqlAlchemyEngineFactory` | Classe | `factories.sqlalchemy_engine_factory` | FEAT-001.2 |
| `SqlAlchemySessionFactory` | Classe | `factories.sqlalchemy_session_factory` | FEAT-001.2 |
| `AuthOrmValueConverter` | Classe | `mappers.auth_orm_value_converter` | FEAT-002.1 |
| `AuthTableNamingConvention` | Classe | `naming.auth_table_naming_convention` | FEAT-001.3 |
| `SqlAlchemyAuthUnitOfWork` | Classe | `unit_of_work.sqlalchemy_auth_unit_of_work` | FEAT-003.2 |
| `AuthCatalogBootstrap` | Classe | `bootstrap.auth_catalog_bootstrap` | FEAT-005.2 |
| `AuthDatabaseCli` | Classe | `cli.auth_database_cli` | FEAT-005.1 |
| `AuthDatabaseMappingError` | Exception | `exceptions.mapping` | FEAT-002.1 |
| `AuthDatabasePersistenceError` | Exception | `exceptions.persistence` | FEAT-003.1 |

## Hors contrat public (internes)

Repositories SQLAlchemy, modèles ORM, mappers spécialisés et scripts Alembic
ne sont pas exportés dans ``__all__`` ; ils peuvent évoluer sans bump majeur.

## Règle de rupture de contrat

- Suppression d'un symbole public → **MAJOR bump**
- Changement de signature incompatible → **MAJOR bump**
- Ajout d'un symbole → **MINOR bump**
- Correction de comportement sans rupture → **PATCH bump**
