# Assignment — BL-003

| Champ | Valeur |
|-------|--------|
| **ID** | BL-003 |
| **Titre** | Migrations Alembic et cohérence schéma |
| **Version** | v0.1.0 |
| **Priorité** | P0 |
| **FEAT** | FEAT-002.2, FEAT-002.3 |
| **US** | US-003 — Migrations et cohérence schéma |
| **Dépendances** | BL-002 |

## Périmètre

- `AlembicConfigFactory`, `AuthDatabaseMigrator`
- `MigrationOrmConsistencyChecker`
- `env.py`, `script.py.mako`, révision `0001_initial_auth_schema`
- Test contrat migration ↔ ORM

## Hors périmètre

CLI utilisateur (`baobab-auth-db migrate`) — BL-007.
