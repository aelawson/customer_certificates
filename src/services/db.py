import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.services.caching_query import query_callable
from src.services.cache import Cache
from src.services.config import Config

class DBService:
    """
    Service encapsulating logic and instantiation of the database backend.
    """

    def __init__(self):
        self.engine = self.get_db_engine()

    def get_db_connection_str(self):
        """
        Returns db connection string based on env.
        """
        # Hardcode tst env db connection to use SQLLite
        if os.environ.get('env') == 'tst':
            return 'sqlite:////opt/app/test.db'
        else:
            return '{engine}://{user}:{pass}@{host}:{port}/{db}'.format(
                **Config['db']
            )

    def get_db_engine(self):
        """
        Creates and returns a db engine based on the connection string generated.
        """
        connection_str = self.get_db_connection_str()
        return create_engine(connection_str)

    def get_db_session(self):
        """
        Creates and returns a scoped session (for the request session).
        """
        return scoped_session(
            sessionmaker(
                bind=self.engine,
                query_cls=query_callable(Cache.regions)
            )
        )

DB = DBService()
