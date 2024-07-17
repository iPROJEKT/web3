from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from bot.core.db import Base


class User(Base):
    user_id = Column(Integer, unique=True, nullable=False)
    seed_phrase = Column(String, unique=True, nullable=False)
    private_key = Column(String, unique=True, nullable=False)
    public_key = Column(String, unique=True, nullable=False)
    six_code = Column(Integer, unique=True, nullable=False)
    address = Column(String, unique=True, nullable=False)
    reservations = relationship('UserDepozit')


class UserDepozit(Base):
    user_id = Column(Integer, ForeignKey('user.user_id'))
    amount = Column(Integer, unique=True, nullable=False)
    created_at = Column(DateTime)
    status = Column(Boolean)
    id_transaction = Column(Integer, unique=True, nullable=False)
    token_id = Column(Integer, unique=True, nullable=False)


class Transaction(Base):
    from_user = Column(Integer, unique=True, nullable=False)
    to_user = Column(Integer, unique=True, nullable=False)
    amount = Column(Integer, unique=True, nullable=False)
    tx_hash_hex = Column(String, unique=True, nullable=True)
