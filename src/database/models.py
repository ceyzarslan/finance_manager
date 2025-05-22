from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    created_at = Column(Date, default=datetime.utcnow)
    
    transactions = relationship('Transaction', back_populates='user')

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String(10), nullable=False)  # 'income' or 'expense'
    category = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    note = Column(String(200))
    date = Column(Date, nullable=False, default=datetime.utcnow)
    
    user = relationship('User', back_populates='transactions')

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    type = Column(String(10), nullable=False)  # 'income' or 'expense'
    description = Column(String(200))

def init_db(db_url):
    """Initialize the database with tables"""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return engine 