# Handoff — BL-002

## État

| Champ | Valeur |
|-------|--------|
| Backlog | BL-002 |
| Statut | TECH_REVIEW_PASSED |
| Prochain backlog | BL-003 (migrations) |

## Réalisé

- 9 modèles ORM + base + registry.
- 10 tests, create_all SQLite validé.
- Revue PO → Architecte → QA → Relecteur complétée.

## Pour BL-003

- Utiliser `AuthOrmRegistry.models()` comme `target_metadata` Alembic.
- Générer révision `0001_initial_auth_schema` reflétant les modèles.
- Implémenter `MigrationOrmConsistencyChecker`.

## Dette

- Retirer contrainte `uq_auth_sessions_session_id` (optionnel, refactor).
- Tests PostgreSQL → BL-005/BL-008.
