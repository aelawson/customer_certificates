from sqlalchemy import Column, Integer, SmallInteger, LargeBinary, Text

from src.models import Base

class Certificate(Base):
    __tablename__ = 'certificates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    private_key = Column(LargeBinary)
    active = Column(SmallInteger)
    body = Column(Text)

    def __repr__(self):
        return "Certificate<(id={id}, user_id={user_id}, active={active})>".format(
            id=self.id,
            user_id=self.user_id,
            active=self.active
        )
