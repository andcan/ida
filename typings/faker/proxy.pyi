"""
This type stub file was generated by pyright.
"""

import random


class Faker(object):
    """Proxy class capable of supporting multiple locales"""
    cache_pattern = ...
    generator_attrs = ...

    def __init__(self, locale=..., providers=..., generator=..., includes=..., **config) -> None:
        ...

    def __getitem__(self, locale):
        ...

    def __getattribute__(self, attr):
        """
        Handles the "attribute resolution" behavior for declared members of this proxy class

        The class method `seed` cannot be called from an instance.

        :param attr: attribute name
        :return: the appropriate attribute
        """
        ...

    def __getattr__(self, attr):
        """
        Handles cache access and proxying behavior

        :param attr: attribute name
        :return: the appropriate attribute
        """
        ...

    @classmethod
    def seed(cls, seed=...):
        """
        Seeds the shared `random.Random` object across all factories

        :param seed: seed value
        """
        ...

    def seed_instance(self, seed=...):
        """
        Creates and seeds a new `random.Random` object for each factory

        :param seed: seed value
        """
        ...

    def seed_locale(self, locale, seed=...):
        """
        Creates and seeds a new `random.Random` object for the factory of the specified locale

        :param locale: locale string
        :param seed: seed value
        """
        ...

    @property
    def random(self):
        """
        Proxies `random` getter calls

        In single locale mode, this will be proxied to the `random` getter
        of the only internal `Generator` object. Subclasses will have to
        implement desired behavior in multiple locale mode.
        """
        ...

    @random.setter
    def random(self, value):
        """
        Proxies `random` setter calls

        In single locale mode, this will be proxied to the `random` setter
        of the only internal `Generator` object. Subclasses will have to
        implement desired behavior in multiple locale mode.
        """
        ...

    @property
    def locales(self):
        ...

    @property
    def weights(self):
        ...

    @property
    def factories(self):
        ...

    def items(self):
        ...

    def first_name(self) -> str:
        ...

    def last_name(self) -> str:
        ...

    def name(self) -> str:
        ...

    def ssn(self) -> str:
        ...
