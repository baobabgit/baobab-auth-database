FEAT-003.2 — SqlAlchemyAuthUnitOfWork
=====================================

:Rattachée à: :ref:`us-003-repositories-uow`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §8
:Implémentation: :class:`baobab_auth_database.unit_of_work.sqlalchemy_auth_unit_of_work.SqlAlchemyAuthUnitOfWork`

Description
-----------

Unit of Work synchrone exposant tous les repositories et gérant commit/rollback.

Critères d'acceptation
----------------------

#. Implémente le protocole ``UnitOfWork`` du core.
#. Expose users, profiles, roles, permissions, sessions, audit, jwk_keys.
#. Tests commit et rollback.

Tâches
------

* ``TASK-003.2.1`` Implémenter ``SqlAlchemyAuthUnitOfWork``.
* ``TASK-003.2.2`` Tests UoW commit/rollback.
