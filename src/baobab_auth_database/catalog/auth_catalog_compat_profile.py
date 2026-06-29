"""Profils de compatibilité catalogue RBAC.

:spec: FEAT-006.2
"""

from importlib.metadata import PackageNotFoundError, version


class AuthCatalogCompatProfile:
    """Profils figés alignés sur la dépendance ``baobab-auth-core`` installée.

    :spec: FEAT-006.2
    """

    CORE_051: str = "core_051"

    SUPPORTED: frozenset[str] = frozenset({CORE_051})

    @classmethod
    def default(cls) -> str:
        """Retourne le profil par défaut pour la dépendance courante.

        :returns: Identifiant du profil actif.
        """
        return cls.CORE_051

    @classmethod
    def validate(cls, profile: str) -> str:
        """Valide un profil demandé.

        :param profile: Identifiant de profil CLI.
        :returns: Profil validé.
        :raises ValueError: Si le profil est inconnu.
        """
        if profile not in cls.SUPPORTED:
            supported = ", ".join(sorted(cls.SUPPORTED))
            msg = f"Profil inconnu {profile!r} ; profils supportés : {supported}"
            raise ValueError(msg)
        return profile

    @classmethod
    def installed_core_version(cls) -> str:
        """Lit la version PyPI de ``baobab-auth-core``.

        :returns: Version semver du core installé.
        :raises RuntimeError: Si le package core est absent.
        """
        try:
            return version("baobab-auth-core")
        except PackageNotFoundError as exc:
            msg = "baobab-auth-core n'est pas installé"
            raise RuntimeError(msg) from exc
