# ADR-002 — Catalogue RBAC versionné v0.2.0

## Statut

Accepté — 2026-06-28

## Contexte

La v0.2.0 exige de prouver quel catalogue RBAC a été appliqué, de détecter les
dérives sans modifier la base, et d'exposer des diagnostics CLI.

Le CDC mentionne le profil `core_080` et une dépendance `baobab-auth-core>=0.8.0`,
alors que la v0.1.0 validée repose sur PyPI `0.5.1`.

## Décision

1. **Table `auth_catalog_versions`** — trace append-only après chaque seed réussi.
2. **Checksum SHA-256** — sérialisation déterministe permissions + rôles + mappings.
3. **Profil actif `core_051`** — aligné sur la dépendance réelle `>=0.5.1,<0.6.0`.
   Le profil `core_080` sera activé lors du bump core `0.8.x`.
4. **Seed non destructif** — ajout des manquants + resync mappings rôles système ;
   les permissions obsolètes en base ne sont pas supprimées automatiquement.
5. **CLI** — `catalog check|seed|report` ; `bootstrap` conservé comme alias de seed.

## Conséquences

- Pas de rupture de l'API publique v0.1.0 (`__all__` inchangé).
- Migration `0002` obligatoire avant seed catalogue v0.2.0.
- Validation inter-librairies continue sur core `0.5.1` jusqu'à bump explicite.
