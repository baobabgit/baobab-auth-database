# Prompts de rôle — BL-005

## Product Owner (Spec → Design)

Valider FEAT-003.1 : chaque port core couvert, tests unicité CDC, SQLite mémoire.

## Architecte (Design → In progress)

Mapper FEAT → 8 classes repository + `SqlAlchemyPersistenceGuard` +
`AuthDatabasePersistenceError`. Session SQLAlchemy injectée (composition UoW).

## Développeur (In progress → In review)

TDD miroir `tests/unit/baobab_auth_database/repositories/`, docstrings RST,
`black` / `ruff` / `mypy` / `pytest ≥ 95 %`.

## Ingénieur QA (In review)

22 tests repositories, couverture globale 96,34 %, unicité 6 contraintes CDC.

## Relecteur (In review → TECH_REVIEW_PASSED)

Conformité ports core, pas de secret en logs, sync tables pivot user_roles /
role_permissions, décision sécurité.
