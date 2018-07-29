import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.services.config import Config

class DBService:

    @classmethod
    def get_db_connection_str(cls):
        if os.environ.get('env') == 'tst':
            return 'sqlite:////opt/app/test.db'
        else:
            return '{engine}://{user}:{pass}@{host}:{port}/{db}'.format(
                **Config['db']
            )

    @classmethod
    def get_db_session(cls):
        connection_str = cls.get_db_connection_str()
        engine = create_engine(connection_str)

        return scoped_session(sessionmaker(bind=engine))
