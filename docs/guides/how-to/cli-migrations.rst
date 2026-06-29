Comment utiliser la CLI migrations
====================================

:spec: FEAT-005.1

Prérequis
---------

Configurer la base via ``AUTH_DB_DATABASE_URL`` (voir ``AuthDatabaseSettings``).

Installation
------------

.. code-block:: bash

   uv sync
   uv run baobab-auth-db --help

Commandes
---------

``upgrade``
   Applique toutes les migrations Alembic jusqu'à ``head``.

``downgrade``
   Annule toutes les migrations (retour à ``base``).

``current``
   Affiche la révision courante (ou ``base`` si vierge).

``history``
   Liste les identifiants de révision connus.

``bootstrap``
   Seed idempotent des rôles et permissions ``DefaultAuthCatalog`` du core.

Exemple
-------

.. code-block:: bash

   export AUTH_DB_DATABASE_URL="sqlite:///./auth.db"
   uv run baobab-auth-db upgrade
   uv run baobab-auth-db bootstrap
   uv run baobab-auth-db current
