from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from database import Base

from datetime import datetime, timezone

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    # nullable define se uma coluna pode ou não aceitar valores nulos 
    # no banco de dados. Se omitido, fica definido em 'nullable=True'.
    # Equivale ao NOT NULL no SQL
    username = Column(String(length=50), unique=True, nullable=False) # <-- a coluna username deve sempre ter um valor
    email = Column(String(length=100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc)) # <-- a coluna created_at pode ficar vazia
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))


class Word(Base):
    __tablename__ = 'words'
    word_id = Column(Integer, primary_key=True)
    word = Column(String, unique=True, nullable=False)
    meaning = Column(Text, nullable=False)
    example = Column(Text)
    created_by = Column(ForeignKey('users.user_id', ondelete='SET NULL'))
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))