from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Explicitly define the * exports
__all__ = ['user', 'certificate']