# Handoff — BL-005

## État

| Champ | Valeur |
|-------|--------|
| Backlog | BL-005 |
| Statut | TECH_REVIEW_PASSED |
| Gates | Spec ✓ Design ✓ Dev ✓ QA ✓ Review ✓ |
| Prochain backlog | BL-006 — SqlAlchemyAuthUnitOfWork |

## HANDOFF (format workflow)

```
task: TASK-003.1.1 / TASK-003.1.2 / TASK-003.1.3
role_done: Relecteur
status: In review -> TECH_REVIEW_PASSED
branch: bl/005-repositories-sync (merge 1a4fc3b sur version/v0.1.0)
commit: 68ee61b
verify: uv run pytest --cov=src --cov-fail-under=95 -q
---
Fait ce tour-ci : 8 repositories synchrones, 22 tests, merge version/v0.1.0.
Prochaine action : BL-006 — implémenter SqlAlchemyAuthUnitOfWork exposant users,
profiles, roles, permissions, sessions, audit, jwk_keys + commit/rollback.
Décisions : sync pivot explicite ; repositories hors __all__ jusqu'à BL-008 ;
IntegrityError -> AuthDatabasePersistenceError via guard.
Blocages : aucun.
```

## Réalisé

- Ports core 0.5.1 implémentés + profils + JWK.
- Qualité : 75 tests, 96,34 % couverture.
- Workflow PO → Architecte → Dev → QA → Relecteur complété (2026-06-29).

## Pour BL-006

- Instancier les repositories avec la session UoW.
- Exposer propriétés `users`, `profiles`, `roles`, etc. sur le UoW.
- Tests commit / rollback transactionnels.

## Process (écarts clos 2026-06-29)

- `uv run nox -s all` : PASS.
- PR [#9](https://github.com/baobabgit/baobab-auth-database/pull/9) : CI verte, mergée.
- Release manager : hors périmètre (version non `RELEASE_READY`).

## Dette process

- Ouvrir PR `bl/006-...` → `version/v0.1.0` **avant** merge (process strict dès BL-006).

## Commandes de reprise

```bash
uv sync
uv run pytest tests/unit/baobab_auth_database/repositories/ -q
uv run python scripts/check_traceability.py
```
