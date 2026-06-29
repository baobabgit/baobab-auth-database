# Rapport d'intégration — baobab-auth-core v0.5.1 × baobab-auth-database v0.2.0

Date : 2026-06-28  
Producteur : baobab-auth-database  
Consommateur : baobab-auth-core (PyPI 0.5.1)  
Méthode : pypi + tests contrat et catalogue  
Résultat : **PASSED**

## Périmètre validé

- Import ``DefaultAuthCatalog`` depuis ``baobab_auth_core.domain.catalogs``.
- Seed idempotent + resync mappings rôles système.
- Checksum déterministe aligné sur le catalogue core installé.
- Diagnostics : permissions/rôles manquants ou obsolètes, mappings divergents.
- Rôle ``SERVICE`` sans permission ; ``SUPER_ADMIN`` avec toutes les permissions core.
- CLI ``catalog check|seed|report`` sur SQLite migré (révision ``0002``).

## Commandes exécutées

```bash
uv run nox -s all
uv run pytest tests/contracts/ tests/integration/test_catalog_cli_integration.py -q
```

## Notes

- Profil actif : ``core_051`` (dépendance réelle ``>=0.5.1,<0.6.0``).
- Le profil ``core_080`` du CDC sera activé lors du bump core ``0.8.x``.
