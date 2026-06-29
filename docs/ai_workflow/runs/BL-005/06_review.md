# Revue technique — BL-005

**Relecteur** : relecteur  
**Date** : 2026-06-29  
**Verdict** : **APPROUVÉ**

## Checklist AGENTS.md

| Critère | Statut |
|---------|--------|
| 1 classe = 1 fichier | OK (9 classes) |
| Type hints complets | OK |
| Docstrings RST + `:spec: FEAT-003.1` | OK |
| Tests miroir | OK (8 fichiers) |
| black / ruff / mypy | OK |
| Couverture ≥ 95 % (global) | OK (96,34 %) |
| Pas de secret en clair | OK |

## Conformité ports core (0.5.1)

| Port | Implémentation | Méthodes clés |
|------|----------------|---------------|
| `UserRepository` | `SqlAlchemyUserRepository` | get/save/delete, roles sync |
| `RoleRepository` | `SqlAlchemyRoleRepository` | list, count_users_with_role |
| `PermissionRepository` | `SqlAlchemyPermissionRepository` | list_permissions |
| `SessionRepository` | `SqlAlchemySessionRepository` | refresh_token_id lookup |
| `AuditRepository` | `SqlAlchemyAuditRepository` | append-only |

## Points positifs

- Composition session + mappers : prêt pour UoW BL-006.
- Erreurs d'intégrité encapsulées (`AuthDatabasePersistenceError`).
- Tables pivot synchronisées explicitement (aligné ADR-001).
- Tests unicité couvrent le CDC §8.

## Observations (non bloquantes)

1. **PR GitHub** : merge direct `bl/` → `version/` sans PR CI — dette process
   (à formaliser pour BL-006+).
2. **Export `__all__`** : repositories hors contrat public — OK pour BL-005, suivi BL-008.
3. **PostgreSQL** : non testé en natif — MVP SQLite ; intégration PG → BL-008.
4. **Datetime SQLite** : tzinfo perdu au roundtrip — documenté QA ; acceptable MVP.

## Sécurité (déclencheur)

Surface : persistance `password_hash`, `refresh_token_hash`, clés JWK chiffrées.

| Contrôle | Résultat |
|----------|----------|
| bandit | OK |
| repr ORM sans secrets | OK (BL-002) |
| Gate Security | **skipped** — pas de surface HTTP ; revue bandit suffisante MVP |

## Décision

**APPROUVÉ** — BL-005 ISO FEAT-003.1 et critères backlog.
