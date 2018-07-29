import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.services.config import Config

class DBService:

    def __init__(self):
        self.engine = self.get_db_engine()

    def get_db_connection_str(self):
        if os.environ.get('env') == 'tst':
            return 'sqlite:////opt/app/test.db'
        else:
            return '{engine}://{user}:{pass}@{host}:{port}/{db}'.format(
                **Config['db']
            )

    def get_db_engine(self):
        connection_str = self.get_db_connection_str()
        return create_engine(connection_str)

    def get_db_session(self):
        return scoped_session(sessionmaker(bind=self.engine))

DB = DBService()
