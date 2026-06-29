FEAT-005.2 — Bootstrap catalogue core
=====================================

:Rattachée à: :ref:`us-005-cli-bootstrap`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4, §6
:Implémentation: :class:`baobab_auth_database.bootstrap.auth_catalog_bootstrap.AuthCatalogBootstrap`

Description
-----------

Bootstrap idempotent des rôles et permissions depuis ``DefaultAuthCatalog``.

Critères d'acceptation
----------------------

#. Idempotent : second appel sans doublon.
#. Importe ``DefaultAuthCatalog`` depuis le core uniquement.
#. Tests d'intégration bootstrap sur SQLite.

Tâches
------

* ``TASK-005.2.1`` Implémenter ``AuthCatalogBootstrap``.
