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
        self.regions[region].configure(
            "dogpile.cache.redis",
            arguments={
                'host': Config['cache']['host'],
                'port': Config['cache']['port'],
                'db': Config['cache']['db'],
                'redis_expiration_time': Config['cache']['ttl']
            }
        )

Cache = CacheService()
Cache.set_cache_region_config('default')
