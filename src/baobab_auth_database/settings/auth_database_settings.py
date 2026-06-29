"""Configuration typée de la persistance auth.

:spec: FEAT-001.1
"""

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_SUPPORTED_BASE_SCHEMES = frozenset({"sqlite", "postgresql"})


class AuthDatabaseSettings(BaseSettings):
    """Paramètres injectables pour SQLAlchemy et Alembic.

    Les secrets (URL de base) ne sont jamais exposés dans ``repr()``.

    :param database_url: URL SQLAlchemy complète.
    :param echo_sql: Active l'écho SQL (développement uniquement).
    :param pool_size: Taille du pool de connexions (PostgreSQL).
    :param max_overflow: Connexions supplémentaires au-delà du pool.
    :spec: FEAT-001.1
    """

    model_config = SettingsConfigDict(
        env_prefix="AUTH_DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: SecretStr = Field(
        default=SecretStr("sqlite:///:memory:"),
        description="URL SQLAlchemy (sqlite ou postgresql).",
    )
    echo_sql: bool = Field(default=False, description="Écho des requêtes SQL.")
    pool_size: int = Field(default=5, ge=1, description="Taille du pool.")
    max_overflow: int = Field(default=10, ge=0, description="Overflow du pool.")

    @field_validator("database_url")
    @classmethod
    def validate_database_url_scheme(cls, value: SecretStr) -> SecretStr:
        """Valide que l'URL utilise un schéma supporté.

        :param value: URL à valider.
        :returns: L'URL inchangée si valide.
        :raises ValueError: Si le schéma n'est pas supporté.
        """
        raw = value.get_secret_value()
        scheme = raw.split("://", maxsplit=1)[0].lower()
        base_scheme = scheme.split("+", maxsplit=1)[0]
        if base_scheme not in _SUPPORTED_BASE_SCHEMES:
            supported = ", ".join(sorted(_SUPPORTED_BASE_SCHEMES))
            msg = (
                f"Schéma SQLAlchemy non supporté : {scheme!r}. "
                f"Attendu : {supported} (+ driver optionnel)."
            )
            raise ValueError(msg)
        return value

    def resolved_database_url(self) -> str:
        """Retourne l'URL de base en clair pour SQLAlchemy.

        :returns: URL SQLAlchemy dévoilée.
        """
        return self.database_url.get_secret_value()

    def __repr__(self) -> str:
        """Représentation sans secret.

        :returns: Chaîne décrivant la configuration sans l'URL.
        """
        return (
            f"{self.__class__.__name__}("
            f"database_url='***', "
            f"echo_sql={self.echo_sql!r}, "
            f"pool_size={self.pool_size!r}, "
            f"max_overflow={self.max_overflow!r})"
        )
