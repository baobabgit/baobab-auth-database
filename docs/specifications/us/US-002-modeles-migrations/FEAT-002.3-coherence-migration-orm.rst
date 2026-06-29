FEAT-002.3 — Cohérence migration ↔ modèles ORM
================================================

:Rattachée à: :ref:`us-002-modeles-migrations`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §9
:Implémentation: test automatisé ``tests/contracts/test_migration_orm_consistency.py``

Description
-----------

Test automatisé vérifiant que le schéma migré contient toutes les colonnes
utilisées par les modèles ORM.

Critères d'acceptation
----------------------

#. Test échoue si une colonne ORM manque dans le schéma migré.
#. Exécuté en CI sur SQLite ; PostgreSQL en intégration si disponible.

Tâches
------

* ``TASK-002.3.1`` Harness de comparaison schéma ↔ modèles.
