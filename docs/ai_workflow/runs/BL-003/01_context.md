# Context — BL-003

## Prérequis

Modèles ORM et registry (BL-002) stables.

## Objectif

Permettre upgrade/downgrade reproductible du schéma auth et garantir l'alignement
entre scripts Alembic et modèles SQLAlchemy.

## Références

- FEAT-002.2, FEAT-002.3
- ADR-001 § migrations
