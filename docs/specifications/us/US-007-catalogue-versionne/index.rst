US-007 — Catalogue RBAC versionné
===================================

:spec: CDC v0.2.0

Objectif
--------

Persister et diagnostiquer le catalogue RBAC core avec checksum, profil de
compatibilité et commandes CLI.

Features
--------

.. toctree::
   :maxdepth: 1

   FEAT-006.1-auth-catalog-versions
   FEAT-006.2-catalog-checksum
   FEAT-006.3-catalog-diagnostics
   FEAT-006.4-catalog-seed-version
   FEAT-006.5-cli-catalog

Critères d'acceptation
----------------------

#. La base enregistre chaque seed catalogue réussi.
#. ``catalog check`` détecte les divergences sans écrire.
#. Le profil ``core_051`` correspond au core PyPI ``0.5.1``.
