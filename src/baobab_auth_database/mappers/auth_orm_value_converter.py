"""Conversion sécurisée de valeurs ORM vers value objects core.

:spec: FEAT-004.1
"""

from collections.abc import Callable
from enum import StrEnum
from typing import TypeVar

from baobab_auth_core.exceptions.validation import ValidationError

from baobab_auth_database.exceptions.mapping.auth_database_mapping_error import (
    AuthDatabaseMappingError,
)

_E = TypeVar("_E", bound=StrEnum)
_T = TypeVar("_T")


class AuthOrmValueConverter:
    """Utilitaires partagés pour le mapping ORM → domaine.

    :spec: FEAT-004.1
    """

    @staticmethod
    def require_non_empty(value: str, field: str) -> str:
        """Valide qu'une chaîne ORM n'est pas vide.

        :param value: Valeur lue en base.
        :param field: Nom du champ (diagnostic).
        :returns: La valeur si non vide.
        :raises AuthDatabaseMappingError: Si la valeur est vide.
        """
        if not value or not value.strip():
            msg = f"Champ obligatoire vide : {field}."
            raise AuthDatabaseMappingError(msg)
        return value

    @staticmethod
    def to_enum(enum_cls: type[_E], raw: str, field: str) -> _E:
        """Convertit une chaîne ORM en enum StrEnum du core.

        :param enum_cls: Classe enum cible.
        :param raw: Valeur stockée en base.
        :param field: Nom du champ (diagnostic).
        :returns: Membre de l'enum.
        :raises AuthDatabaseMappingError: Si la valeur est inconnue.
        """
        try:
            return enum_cls(raw)
        except ValueError as exc:
            msg = f"Valeur enum invalide pour {field} : {raw!r}."
            raise AuthDatabaseMappingError(msg, cause=exc) from exc

    @staticmethod
    def wrap_validation(field: str, factory: Callable[[], _T]) -> _T:
        """Exécute une factory VO et transforme ``ValidationError`` en mapping error.

        :param field: Nom du champ (diagnostic).
        :param factory: Callable retournant un value object.
        :returns: Résultat de la factory.
        :raises AuthDatabaseMappingError: Si la validation core échoue.
        """
        try:
            return factory()
        except ValidationError as exc:
            msg = f"Validation core échouée pour {field}."
            raise AuthDatabaseMappingError(msg, cause=exc) from exc
