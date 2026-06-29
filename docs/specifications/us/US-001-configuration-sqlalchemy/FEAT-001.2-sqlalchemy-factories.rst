FEAT-001.2 — Factories SQLAlchemy engine et session
=================================================

:Rattachée à: :ref:`us-001-configuration-sqlalchemy`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4
:Implémentation: :class:`baobab_auth_database.factories.sqlalchemy_engine_factory.SqlAlchemyEngineFactory`

Description
-----------

Factories orientées objet pour créer l'engine SQLAlchemy et les sessions
à partir de ``AuthDatabaseSettings``.

Critères d'acceptation
----------------------

#. ``SqlAlchemyEngineFactory`` produit un engine configuré (pool, echo).
#. ``SqlAlchemySessionFactory`` produit des sessions liées à l'engine.
#. Compatible SQLite mémoire pour les tests unitaires.
#. Convention de nommage des tables ``auth_*`` centralisée.

Tâches
------

* ``TASK-001.2.1`` Implémenter ``SqlAlchemyEngineFactory``.
* ``TASK-001.2.2`` Implémenter ``SqlAlchemySessionFactory``.
* ``TASK-001.2.3`` Tests factories sur SQLite mémoire.
