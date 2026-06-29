# Prompts de rôle — BL-006

## Product Owner (Spec → Design)

Valider FEAT-003.2 : protocole `UnitOfWork`, 7 repositories exposés, tests
commit/rollback CDC §9.

## Architecte (Design → In progress)

Une classe `SqlAlchemyAuthUnitOfWork` ; injection `SqlAlchemySessionFactory` ;
repositories lazy sur session unique ; rollback implicite si exception dans le contexte.

## Développeur (In progress → In review)

TDD miroir `tests/unit/baobab_auth_database/unit_of_work/`, docstrings RST,
`uv run nox -s all`, PR ouverte **avant** merge.

## Ingénieur QA (In review)

7 tests UoW, couverture globale ≥ 95 %, protocole core vérifié via `isinstance`.

## Relecteur (In review → TECH_REVIEW_PASSED)

Conformité FEAT-003.2, session lifecycle, pas de fuite session, CI verte.
