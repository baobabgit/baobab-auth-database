US-005 — CLI et bootstrap catalogue
===================================

:origin: ``01_cdc_v0_1_0_stabilisation_mvp.md`` §4, §8
:Version cible: ``v0.1.0``

Description
-----------

CLI minimale pour migrations et seed ; bootstrap idempotent via ``DefaultAuthCatalog``.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-005.1-cli-migrations
   FEAT-005.2-bootstrap-catalogue

Critères d'acceptation (US)
---------------------------

#. CLI migrations et seed defaults opérationnelles.
#. Bootstrap utilise ``DefaultAuthCatalog`` du core sans catalogue concurrent local.
