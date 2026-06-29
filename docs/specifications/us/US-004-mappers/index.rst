US-004 — Mappers ORM ↔ core
===========================

:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4, §8
:Version cible: ``v0.1.0``

Description
-----------

Conversion bidirectionnelle entre modèles ORM et entités/value objects du core.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-004.1-mappers-entites

Critères d'acceptation (US)
---------------------------

#. Mapper pour chaque entité core utilisée.
#. Erreurs de conversion → ``AuthDatabaseMappingError``.
