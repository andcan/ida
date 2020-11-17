"""
This type stub file was generated by pyright.
"""

class Documentor(object):
    def __init__(self, generator) -> None:
        """
        :param generator: a localized Generator with providers filled,
                          for which to write the documentation
        :type generator: faker.Generator()
        """
        ...
    
    def get_formatters(self, locale=..., excludes=..., **kwargs):
        ...
    
    def get_provider_formatters(self, provider, prefix=..., with_args=..., with_defaults=...):
        ...
    
    @staticmethod
    def get_provider_name(provider_class):
        ...
    


