US-002 — Modèles ORM et migrations Alembic
==========================================

:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4, §8
:Version cible: ``v0.1.0``

Description
-----------

Modèles SQLAlchemy alignés sur le schéma auth et migrations Alembic rejouables.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-002.1-modeles-orm
   FEAT-002.2-migrations-alembic
   FEAT-002.3-coherence-migration-orm

Critères d'acceptation (US)
---------------------------

#. Tables pour users, profiles, roles, permissions, user_roles, role_permissions,
   sessions, audit_events, jwk_keys.
#. Colonnes ``resource``, ``action``, ``is_system``, ``last_used_at``, ``device_label``,
   ``target_type``, ``target_id`` présentes et alignées migrations ↔ modèles.
#. Contraintes uniques sur subject, email, rôle, permission, session, refresh token, kid.
