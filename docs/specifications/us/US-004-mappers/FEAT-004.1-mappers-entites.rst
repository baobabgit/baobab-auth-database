FEAT-004.1 — Mappers entités core
=================================

:Rattachée à: :ref:`us-004-mappers`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §8
:Implémentation: package ``baobab_auth_database.mappers``

Description
-----------

Mappers pour User, UserProfile, Role, Permission, Session, AuditEvent et clés JWK.

Critères d'acceptation
----------------------

#. Tests mappers pour chaque entité core.
#. Aucune duplication des entités core dans ce package.
#. ``AuthDatabaseMappingError`` sur conversion invalide.

Tâches
------

* ``TASK-004.1.1`` Mappers users et profiles.
* ``TASK-004.1.2`` Mappers roles, permissions, sessions, audit, jwk.
