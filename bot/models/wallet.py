from sqlalchemy import Column, Integer, String

from bot.core.db import Base


class User(Base):
    user_id = Column(Integer, unique=True, nullable=False)
    seed_phrase = Column(String, unique=True, nullable=False)
    private_key = Column(String, unique=True, nullable=False)
    public_key = Column(String, unique=True, nullable=False)
    six_code = Column(Integer, unique=True, nullable=False)
    address = Column(String, unique=True, nullable=False)


class Transaction(Base):
    from_user = Column(Integer, unique=True, nullable=False)
    to_user = Column(Integer, unique=True, nullable=False)
    amount = Column(Integer, unique=True, nullable=False)
    tx_hash_hex = Column(String, unique=True, nullable=True)
