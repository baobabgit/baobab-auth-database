# Contrat — Exceptions publiques

> Exceptions publiques de ``baobab-auth-database``.

## Exceptions déclarées

| Exception | Module | Déclenchée par |
|-----------|--------|----------------|
| `AuthDatabaseMappingError` | `exceptions.mapping` | Conversion ORM ↔ domaine invalide |
| `AuthDatabasePersistenceError` | `exceptions.persistence` | Violation d'intégrité SQLAlchemy |

## Notes

Les exceptions publiques font partie du contrat API. Tout changement de leur
liste ou de leurs signatures est soumis aux règles SemVer.
