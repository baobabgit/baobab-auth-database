Diagnostics et synchronisation catalogue RBAC
==============================================

:spec: FEAT-006.5

Prérequis
---------

- Migrations appliquées jusqu'à ``head`` (révision ``0002`` minimum).
- ``baobab-auth-core>=0.5.1,<0.6.0`` installé.
- Variable ``AUTH_DB_DATABASE_URL`` configurée.

Profil de compatibilité
-----------------------

La v0.2.0 utilise le profil ``core_051``, aligné sur la dépendance PyPI réelle.
Le profil ``core_080`` du CDC sera activé lors du bump core ``0.8.x``.

Commandes
---------

``catalog check``
   Compare la base au ``DefaultAuthCatalog`` sans modification.
   Code de sortie ``0`` si conforme, ``1`` si divergent.

``catalog seed``
   Synchronise permissions et rôles manquants ; resynchronise les mappings
   des rôles système. Enregistre une ligne dans ``auth_catalog_versions``.

``catalog report``
   Affiche un rapport texte ou JSON (``--format json``).

Options communes
----------------

``--profile core_051``
   Profil de compatibilité (défaut).

``--format text|json``
   Format de sortie pour ``check`` et ``report``.

``--dry-run``
   Sur ``catalog seed`` : simulation sans écriture.

Exemple
-------

.. code-block:: bash

   uv run baobab-auth-db upgrade
   uv run baobab-auth-db catalog seed
   uv run baobab-auth-db catalog check
   uv run baobab-auth-db catalog report --format json
