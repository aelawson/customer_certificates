from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.services.config import Config

engine = create_engine(
    '{engine}://{user}:{pass}@{host}:{port}/{db}'.format(
        **Config['db']
    )
)

# Create all tables (if they don't exist)
Base.metadata.create_all(engine)

DbSession = scoped_session(sessionmaker(bind=engine))