FEAT-005.1 — CLI migrations
=============================

:Rattachée à: :ref:`us-005-cli-bootstrap`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4
:Implémentation: :class:`baobab_auth_database.cli.auth_database_cli.AuthDatabaseCli`

Description
-----------

Point d'entrée CLI pour ``upgrade``, ``downgrade``, ``current``, ``history``.

Critères d'acceptation
----------------------

#. Commandes Alembic exposées via CLI du package.
#. Documentation des commandes dans README et guides.

Tâches
------

* ``TASK-005.1.1`` Implémenter ``AuthDatabaseCli``.
