FEAT-002.1 — Modèles ORM auth
=============================

:Rattachée à: :ref:`us-002-modeles-migrations`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4, §8
:Implémentation: package ``baobab_auth_database.models.orm``

Description
-----------

Un modèle ORM par table auth ; ``repr()`` sans secrets (password_hash, refresh token, clé privée).

Critères d'acceptation
----------------------

#. Modèles pour les 9 entités tables listées dans le CDC.
#. Relations et contraintes uniques conformes au CDC §8.
#. ``repr()`` ne contient jamais de données sensibles.

Tâches
------

* ``TASK-002.1.1`` Modèles users, profiles, roles, permissions.
* ``TASK-002.1.2`` Modèles sessions, audit_events, jwk_keys et tables d'association.
