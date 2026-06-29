FEAT-001.1 — AuthDatabaseSettings
=================================

:Rattachée à: :ref:`us-001-configuration-sqlalchemy`
:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4
:Implémentation: :class:`baobab_auth_database.settings.auth_database_settings.AuthDatabaseSettings`

Description
-----------

Classe de configuration injectable pour la couche persistance : URL de base,
options de pool, echo SQL (développement), préfixe de tables.

Critères d'acceptation
----------------------

#. Chargement depuis variables d'environnement avec préfixe ``AUTH_DB_``.
#. Validation de l'URL SQLAlchemy (schémas ``sqlite`` et ``postgresql`` supportés).
#. ``database_url`` jamais exposée dans ``repr()``.
#. Valeurs par défaut sûres pour le développement local (SQLite mémoire).

Tâches
------

* ``TASK-001.1.1`` Implémenter ``AuthDatabaseSettings``.
* ``TASK-001.1.2`` Tests unitaires settings et absence de secrets dans ``repr()``.
