from sqlalchemy import Column, Integer, String

from src.models import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

    def __repr__(self):
        return "User<(id={id}, name={name}, email={email})>".format(
            id=self.id,
            name=self.name,
            email=self.email
        )
