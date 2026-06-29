# Rapport de tests — BL-005

**Date** : 2026-06-29  
**Périmètre** : repositories synchrones SQLAlchemy  
**Verdict QA** : **PASSED**

## Commandes exécutées

```bash
uv run nox -s all
```

Équivalent `make all` (Windows sans `make`) — session `all` : quality + tests + build +
traceability.

Détail des étapes :

```bash
uv run black --check src tests
uv run ruff check src tests
uv run mypy src
uv run bandit -r src -c pyproject.toml
uv run pytest --cov=src --cov-report=term-missing --cov-fail-under=95
uv build && uv run twine check dist/*
uv run python scripts/check_traceability.py
```

## Résultats outils

| Outil | Résultat |
|-------|----------|
| black | OK |
| ruff | OK |
| mypy (strict) | OK |
| bandit | OK |
| traceability | OK |

## Tests unitaires BL-005 (22)

| Fichier | Tests | Résultat |
|---------|-------|----------|
| `test_sqlalchemy_user_repository.py` | 4 | PASS |
| `test_sqlalchemy_user_profile_repository.py` | 2 | PASS |
| `test_sqlalchemy_role_repository.py` | 3 | PASS |
| `test_sqlalchemy_permission_repository.py` | 2 | PASS |
| `test_sqlalchemy_session_repository.py` | 5 | PASS |
| `test_sqlalchemy_audit_repository.py` | 1 | PASS |
| `test_sqlalchemy_jwk_key_repository.py` | 3 | PASS |
| `test_sqlalchemy_persistence_guard.py` | 2 | PASS |
| **Total périmètre BL-005** | **22** | **PASS** |

## Couverture

| Métrique | Valeur |
|----------|--------|
| Tests projet total | 75 PASS |
| Couverture globale | **96,34 %** |
| Modules repositories | 85–100 % (global ≥ 95 %) |

## Critères FEAT-003.1 vérifiés

| Contrainte unicité | Test |
|--------------------|------|
| `normalized_email` | `test_FEAT_003_1_unicite_email` |
| `auth_subject` | `test_FEAT_003_1_unicite_subject` |
| rôle `name` | `test_FEAT_003_1_unicite_role` |
| permission `name` | `test_FEAT_003_1_unicite_permission` |
| `refresh_token_hash` | `test_FEAT_003_1_unicite_refresh_token` |
| JWK `kid` | `test_FEAT_003_1_unicite_kid` |

## CI GitHub (PR #9)

| Job | Résultat | Run |
|-----|----------|-----|
| Qualité + Typage + Sécurité | PASS | [28350976309](https://github.com/baobabgit/baobab-auth-database/actions/runs/28350976309) |
| Tests + couverture ≥ 95 % | PASS | idem |
| Traçabilité | PASS | idem |
| Politique de commit | PASS | idem |
| Build package | PASS | idem |

PR : [baobabgit/baobab-auth-database#9](https://github.com/baobabgit/baobab-auth-database/pull/9)
(validation rétroactive `bl/005-repositories-sync` → `version/v0.1.0-pre-bl005`, mergée
2026-06-29).

## Observations QA

- SQLite retourne des datetimes naïfs : tests comparent les champs métier, pas
  l'égalité stricte des entités sur les timestamps.
- `uv run nox -s all` exécuté localement (2026-06-29, 18 s, PASS).
