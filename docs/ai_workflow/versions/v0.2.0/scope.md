# Périmètre — v0.2.0

## Objectif

Catalogue RBAC versionné et diagnostics : table `auth_catalog_versions`, checksum
déterministe, commandes CLI `catalog check|seed|report`, profil de compatibilité
`core_051` (core PyPI `0.5.1`).

Source : `docs/specifications/cahier-des-charges/02_cdc_v0_2_0_catalogue_rbac_versionne.md`

## Dépendance core

- PyPI : `baobab-auth-core>=0.5.1,<0.6.0`
- Profil actif : `core_051` (aligné sur la dépendance réelle)
- Le profil `core_080` du CDC sera activé lors du bump core `0.8.x`

## Backlogs inclus

| ID | Titre | Priorité |
|----|-------|---------|
| BL-009 | Table auth_catalog_versions (ORM + migration) | P0 |
| BL-010 | Checksum déterministe et diagnostics catalogue | P0 |
| BL-011 | Bootstrap étendu et enregistrement version catalogue | P0 |
| BL-012 | CLI catalog check, seed, report | P1 |
| BL-013 | Tests, docs et validation v0.2.0 | P1 |

## Backlogs reportés

Aucun — périmètre v0.3.0+ couvert par les cahiers des charges suivants.
