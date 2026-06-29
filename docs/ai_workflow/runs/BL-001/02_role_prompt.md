# Prompts de rôle — BL-001

## Product Owner (Spec)

Vérifier que FEAT-001.1 et FEAT-001.2 couvrent le CDC §4 (configuration, factories)
et que les critères d'acceptation sont testables.

## Architecte (Design)

Valider le mapping FEAT → classes, le contrat `__all__` initial, l'injection
via `AuthDatabaseSettings`, compatibilité SQLite/PostgreSQL.

## Développeur (In progress)

TDD : tests miroir sous `tests/unit/baobab_auth_database/settings/` et
`tests/unit/baobab_auth_database/factories/`.

## Ingénieur QA (In review — tests)

Exécuter `black`, `ruff`, `mypy`, `pytest --cov-fail-under=95`, `bandit`,
`make traceability` sur le périmètre BL-001.

## Relecteur (In review — code)

Revue indépendante vs `AGENTS.md` et critères FEAT-001.1 / FEAT-001.2.
