# Sorties attendues — BL-001

## Code

| Classe | Fichier |
|--------|---------|
| `AuthDatabaseSettings` | `settings/auth_database_settings.py` |
| `SqlAlchemyEngineFactory` | `factories/sqlalchemy_engine_factory.py` |
| `SqlAlchemySessionFactory` | `factories/sqlalchemy_session_factory.py` |
| `AuthTableNamingConvention` | `naming/auth_table_naming_convention.py` |

## Tests (miroir)

- `tests/unit/baobab_auth_database/settings/test_auth_database_settings.py`
- `tests/unit/baobab_auth_database/naming/test_auth_table_naming_convention.py`
- `tests/unit/baobab_auth_database/factories/test_sqlalchemy_factories.py`

## Documentation

- Docstrings RST avec `:spec: FEAT-001.1` ou `FEAT-001.2`
- `.env.example` avec préfixe `AUTH_DB_`

## Qualité

- Couverture globale projet ≥ 95 % (après revue rétroactive : 95,24 %)
- `make traceability` OK
