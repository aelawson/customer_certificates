from dogpile.cache import make_region

from src.services.config import Config

class CacheService:
    """
    Encapsulates cache logic and instantiation
    """

    def __init__(self, regions=None):
        if regions:
            self.regions = { r: make_region() for r in regions }
        else:
            self.regions = { 'default': make_region() }

    def set_cache_region_config(self, region):
        """
        Given a cache region, set it's configuration based on config settings.
        """
        try:
            self.regions[region].configure_from_config({
                'cache.redis.backend': "dogpile.cache.redis",
                'cache.redis.arguments.host': Config['cache']['host'],
                'cache.redis.arguments.port': Config['cache']['port'],
            }, 'cache.redis')
        except KeyError:
            raise Exception('Cache region does not exist.')

Cache = CacheService
