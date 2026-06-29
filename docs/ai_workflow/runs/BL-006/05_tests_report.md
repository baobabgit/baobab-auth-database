# Rapport de tests — BL-006

**Date** : 2026-06-29  
**Périmètre** : SqlAlchemyAuthUnitOfWork  
**Verdict QA** : **PASSED**

## Commandes exécutées

```bash
uv run nox -s all
```

## Résultats outils

| Outil | Résultat |
|-------|----------|
| black | OK |
| ruff | OK |
| mypy (strict) | OK |
| bandit | OK |
| build + twine | OK |
| traceability | OK |

## Tests unitaires BL-006 (7)

| Test | Résultat |
|------|----------|
| `test_FEAT_003_2_satisfies_unit_of_work_protocol` | PASS |
| `test_FEAT_003_2_exposes_all_repositories` | PASS |
| `test_FEAT_003_2_repositories_share_session` | PASS |
| `test_FEAT_003_2_commit_persists_changes` | PASS |
| `test_FEAT_003_2_rollback_discards_uncommitted_changes` | PASS |
| `test_FEAT_003_2_exit_on_exception_rolls_back` | PASS |
| `test_FEAT_003_2_requires_active_context_for_repositories` | PASS |

## Couverture

| Métrique | Valeur |
|----------|--------|
| Tests projet total | 82 PASS |
| Couverture globale | **96,02 %** |
| Module UoW | 93 % |

## CI GitHub (PR #10)

| Job | Résultat | Run |
|-----|----------|-----|
| Qualité + Typage + Sécurité | PASS | [28392519079](https://github.com/baobabgit/baobab-auth-database/actions/runs/28392519079) |
| Tests + couverture ≥ 95 % | PASS | idem |
| Traçabilité | PASS | idem |
| Politique de commit | PASS | idem |
| Build package | PASS | idem |

PR : [baobabgit/baobab-auth-database#10](https://github.com/baobabgit/baobab-auth-database/pull/10)
