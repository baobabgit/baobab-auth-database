# Revue technique — BL-004

**Date** : 2026-06-28  
**Verdict** : **APPROUVÉ** (avec actions de suivi)

## Conformité FEAT-004.1

| Mapper | to_domain | to_model | Erreurs |
|--------|-----------|----------|---------|
| User | OK | OK | partiel |
| Profile | OK | partiel | partiel |
| Role | OK | partiel | OK |
| Permission | OK | OK | OK |
| Session | OK | partiel | OK |
| AuditEvent | OK | partiel | OK |
| JWK | OK (snapshot) | partiel | OK |

## Points positifs

- Isolation claire ORM / domaine — prêt pour repositories BL-005.
- `AuthOrmValueConverter` 100 % testé.
- Mapping `Session.refresh_token_id` ↔ `refresh_token_hash` conforme CDC.
- Snapshot JWK justifié par D1 (core 0.5.1).

## Observations

1. **Couverture par fichier mapper** : 79–90 % sur branches `to_model` except —
   global projet OK ; renforcer avant release si politique stricte par module.
2. **`AuthOrmValueConverter` dans `__all__`** : export public — valider contrat BL-008.
3. **Core version** : D1 documentée ADR-001 ; bump core prévu post-v0.1.0.

## Actions de suivi (non bloquantes)

| ID | Action | Cible | Statut |
|----|--------|-------|--------|
| F4-1 | Tests `to_domain` erreur | BL-004 | **Clos** (2026-06-28) |
| F4-2 | Contrat public mappers | BL-008 | Ouvert |
| F4-3 | Alignement core >=0.8.0 | version ultérieure | Ouvert |

## Décision

**APPROUVÉ** — mappers ISO demande fonctionnelle ; dette couverture `to_model` tracée.
