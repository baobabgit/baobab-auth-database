US-001 — Configuration et infrastructure SQLAlchemy
===================================================

:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4, §8
:Version cible: ``v0.1.0``

Description
-----------

Fournir la configuration typée et les factories SQLAlchemy (engine, session)
nécessaires à la persistance auth sans logique métier locale.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-001.1-auth-database-settings
   FEAT-001.2-sqlalchemy-factories

Critères d'acceptation (US)
---------------------------

#. ``AuthDatabaseSettings`` charge et valide l'URL de base via ``pydantic-settings``.
#. Les factories produisent un engine et des sessions compatibles SQLite et PostgreSQL.
#. Aucun secret n'apparaît dans les logs ou ``repr()`` des objets de configuration.
