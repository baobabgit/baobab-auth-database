# Rapport de tests — BL-001

**Date** : 2026-06-28  
**Périmètre** : configuration, naming, factories SQLAlchemy  
**Verdict QA** : **PASSED**

## Commandes exécutées

```bash
uv run black --check src tests
uv run ruff check src tests
uv run mypy src
uv run bandit -r src -c pyproject.toml
uv run pytest tests/unit/baobab_auth_database/settings/ \
  tests/unit/baobab_auth_database/naming/ \
  tests/unit/baobab_auth_database/factories/ \
  --cov=src/baobab_auth_database/settings \
  --cov=src/baobab_auth_database/naming \
  --cov=src/baobab_auth_database/factories \
  --cov-report=term-missing
make traceability
```

## Résultats

| Outil | Résultat |
|-------|----------|
| black | OK |
| ruff | OK |
| mypy (strict) | OK |
| bandit | OK (0 alerte bloquante) |
| traceability | OK |

## Tests unitaires BL-001

| Fichier | Tests | Résultat |
|---------|-------|----------|
| `test_auth_database_settings.py` | 5 | PASS |
| `test_auth_table_naming_convention.py` | 3 | PASS |
| `test_sqlalchemy_factories.py` | 4 | PASS |
| **Total périmètre BL-001** | **12** | **PASS** |

## Couverture (modules BL-001)

| Module | Couverture |
|--------|------------|
| `auth_database_settings.py` | 100 % |
| `auth_table_naming_convention.py` | 100 % |
| `sqlalchemy_engine_factory.py` | 100 % |
| `sqlalchemy_session_factory.py` | 100 % |

## Critères FEAT vérifiés

- FEAT-001.1.1 : préfixe env, validation URL, repr sans secret
- FEAT-001.1.2 : rejet schéma non supporté
- FEAT-001.2.1 : engine SQLite mémoire + echo
- FEAT-001.2.2 : session factory opérationnelle
- FEAT-001.2.3 : convention de nommage `auth_*`

## Observations

- Test PostgreSQL réel non exécuté (SQLite suffisant pour BL-001 ; intégration PG prévue BL-005/BL-008).
- Couverture globale projet (47 tests, 95,24 %) inclut les BL suivants — non régressif.
