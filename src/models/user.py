from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.models import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    certificates = relationship("Certificate", backref="users", passive_deletes=True)

    def __repr__(self):
        return "User<(id={id}, name={name}, email={email})>".format(
            id=self.id,
            name=self.name,
            email=self.email
        )
