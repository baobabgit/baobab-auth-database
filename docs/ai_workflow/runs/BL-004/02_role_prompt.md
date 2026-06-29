# Prompts de rôle — BL-004

## Product Owner

Valider mapping champs CDC, roundtrip domaine, erreurs typées, compatibilité core 0.5.1.

## Architecte

Valider séparation converter / mappers, passage rôles-permissions en paramètres
(pas de lazy load), snapshot JWK.

## QA

19 tests mappers, couverture globale ≥ 95 %, cas erreur `AuthDatabaseMappingError`.

## Relecteur

Vérifier branches `to_model` non couvertes, export `__all__`, mapping refresh_token.
