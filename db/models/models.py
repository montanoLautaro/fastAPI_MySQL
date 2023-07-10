from sqlalchemy import Column, Integer, String, Boolean, SmallInteger, ForeignKey
from db.config.client import Base
from sqlalchemy.orm import relationship
from db.config.client import engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    entertainments = relationship("Entertainment", back_populates="user")


class Entertainment(Base):
    __tablename__ = "entertainments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250), nullable=False)
    type = Column(String(250), nullable=False)
    review = Column(String(255))
    image = Column(String(255))
    duration = Column(Integer)
    score = Column(SmallInteger)
    repeat = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="entertainments")


Base.metadata.create_all(bind=engine)
