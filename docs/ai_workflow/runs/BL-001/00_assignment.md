# Assignment — BL-001

| Champ | Valeur |
|-------|--------|
| **ID** | BL-001 |
| **Titre** | Configuration AuthDatabaseSettings et factories SQLAlchemy |
| **Version** | v0.1.0 |
| **Priorité** | P0 |
| **FEAT** | FEAT-001.1, FEAT-001.2 |
| **US** | US-001 — Configuration et infrastructure SQLAlchemy |
| **Origin** | `01_cdc_v0_1_0_stabilisation_mvp.md` §4 |
| **Dépendances** | Aucune |

## Périmètre assigné

- Renommer le package `example_package` → `baobab_auth_database`
- `AuthDatabaseSettings` (pydantic-settings, préfixe `AUTH_DB_`)
- `SqlAlchemyEngineFactory`, `SqlAlchemySessionFactory`
- `AuthTableNamingConvention` (préfixe `auth_`, conventions Alembic)

## Hors périmètre

Modèles ORM, migrations, repositories (BL-002+).
