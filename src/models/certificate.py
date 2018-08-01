from sqlalchemy import Column, Integer, Boolean, LargeBinary, Text
from sqlalchemy.schema import ForeignKey, Index

from src.models import Base
from src.models.user import User

class Certificate(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    private_key = Column(LargeBinary, nullable=False)
    active = Column(Boolean, nullable=False)
    body = Column(Text, nullable=False)

    __table_args__ = (Index('user_id_and_id_index', "user_id", "id"), )

    def __repr__(self):
        return "Certificate<(id={id}, user_id={user_id}, active={active})>".format(
            id=self.id,
            user_id=self.user_id,
            active=self.active
        )
