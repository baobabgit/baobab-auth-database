# Handoff — BL-007

## État

| Champ | Valeur |
|-------|--------|
| Backlog | BL-007 |
| Statut | TECH_REVIEW_PASSED |
| Prochain backlog | BL-008 — Tests contrat core et documentation v0.1.0 |

## HANDOFF

```
role_done: Relecteur
branch: bl/007-cli-bootstrap (PR #11)
commit: 03ad659
---
Fait : CLI baobab-auth-db + AuthCatalogBootstrap idempotent.
Prochaine : BL-008 — tests contrat core, export __all__, doc v0.1.0.
```

## Commandes

```bash
uv run baobab-auth-db upgrade
uv run baobab-auth-db bootstrap
uv run pytest tests/integration/test_auth_catalog_bootstrap_integration.py -q
```
