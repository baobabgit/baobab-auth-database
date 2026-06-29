# Rapport de tests — BL-003

**Date** : 2026-06-28  
**Verdict QA** : **PASSED**

## Tests BL-003

| Fichier | Tests | Résultat |
|---------|-------|----------|
| `test_alembic_config_factory.py` | 2 | PASS |
| `test_auth_database_migrator.py` | 4 | PASS |
| `test_migration_orm_consistency.py` | 4 | PASS |
| **Total** | **10** | **PASS** |

## Couverture modules migrations

| Module | Couverture |
|--------|------------|
| `alembic_config_factory.py` | 100 % |
| `auth_database_migrator.py` | 100 % |
| `migration_orm_consistency_checker.py` | 93 % |
| `0001_initial_auth_schema.py` | 100 % |

Global projet : **95,24 %** (47 tests).

## Scénarios validés

- Upgrade `head` puis downgrade `base` sur SQLite fichier temporaire
- `current()` après upgrade retourne révision `0001`
- `history()` liste la révision initiale
- Contrat : tables ORM ⊆ tables migration, colonnes compatibles

## Observations

- `env.py` omis de la couverture (bootstrap Alembic) — documenté dans `pyproject.toml`.
- CLI non testée — périmètre BL-007.
