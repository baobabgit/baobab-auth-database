FEAT-003.1 — Repositories synchrones
====================================

:Rattachée à: :ref:`us-003-repositories-uow`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4, §8
:Implémentation: package ``baobab_auth_database.repositories``

Description
-----------

Repositories synchrones pour users, profiles, roles, permissions, sessions,
audit et jwk_keys, implémentant les ports du core.

Critères d'acceptation
----------------------

#. Chaque port core a une implémentation SQLAlchemy synchrone.
#. Tests d'unicité email, subject, rôle, permission, session, refresh token, kid.
#. Tests SQLite mémoire pour chaque repository.

Tâches
------

* ``TASK-003.1.1`` ``SqlAlchemyUserRepository`` et profils.
* ``TASK-003.1.2`` Repositories roles, permissions, sessions.
* ``TASK-003.1.3`` Repositories audit et jwk_keys.
