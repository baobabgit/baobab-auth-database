# Context — BL-006

## État au démarrage

- BL-005 mergé sur `version/v0.1.0` : 8 repositories synchrones opérationnels.
- Handoff BL-005 : UoW doit instancier les repositories avec une session partagée.
- Process strict : PR → CI verte → merge (pas de merge direct).

## Objectif

Fournir le point d'entrée transactionnel pour la persistance auth, prêt pour BL-007
(CLI) et BL-008 (contrats publics).

## Références

- FEAT-003.2
- ADR-001 § unit_of_work
- Handoff BL-005
