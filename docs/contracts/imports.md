# Contrat — Imports publics

> Imports garantis stables pour les consommateurs de ``baobab-auth-database``.

## Imports garantis

```python
from baobab_auth_database import (
    AuthCatalogBootstrap,
    AuthDatabaseCli,
    AuthDatabaseMappingError,
    AuthDatabasePersistenceError,
    AuthDatabaseSettings,
    SqlAlchemyAuthUnitOfWork,
    SqlAlchemyEngineFactory,
    SqlAlchemySessionFactory,
)
```

Entry point CLI :

```bash
uv run baobab-auth-db upgrade
uv run baobab-auth-db bootstrap
```

## Imports internes (non garantis)

Les modules ``repositories/``, ``models/orm/``, ``mappers/*_orm_mapper`` et
``migrations/`` sont internes sauf symboles listés dans ``__all__``.
