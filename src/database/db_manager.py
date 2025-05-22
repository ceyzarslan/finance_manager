import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional
from .models import Base, User, Transaction, Category
import pathlib

class DatabaseManager:
    def __init__(self, db_url: str):
        # Ensure the directory exists
        db_path = pathlib.Path(db_url.replace('sqlite:///', ''))
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_transaction(self, user_id: int, type: str, category: str, 
                       amount: float, note: str = None, date: datetime = None) -> Optional[Transaction]:
        """Add a new transaction to the database"""
        try:
            session = self.Session()
            transaction = Transaction(
                user_id=user_id,
                type=type,
                category=category,
                amount=amount,
                note=note,
                date=date or datetime.utcnow()
            )
            session.add(transaction)
            session.commit()
            return transaction
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_transactions(self, user_id: int, start_date: datetime = None, 
                        end_date: datetime = None, category: str = None) -> List[Transaction]:
        """Get transactions with optional filters"""
        try:
            session = self.Session()
            query = session.query(Transaction).filter(Transaction.user_id == user_id)
            
            if start_date:
                query = query.filter(Transaction.date >= start_date)
            if end_date:
                query = query.filter(Transaction.date <= end_date)
            if category:
                query = query.filter(Transaction.category == category)
                
            return query.all()
        finally:
            session.close()

    def get_category_summary(self, user_id: int, start_date: datetime = None, 
                           end_date: datetime = None) -> Dict:
        """Get summary of transactions by category"""
        try:
            session = self.Session()
            transactions = self.get_transactions(user_id, start_date, end_date)
            
            summary = {
                'income': {},
                'expense': {}
            }
            
            for transaction in transactions:
                category_dict = summary[transaction.type]
                if transaction.category not in category_dict:
                    category_dict[transaction.category] = 0
                category_dict[transaction.category] += transaction.amount
                
            return summary
        finally:
            session.close()

    def delete_transaction(self, transaction_id: int, user_id: int) -> bool:
        """Delete a transaction"""
        try:
            session = self.Session()
            transaction = session.query(Transaction).filter(
                Transaction.id == transaction_id,
                Transaction.user_id == user_id
            ).first()
            
            if transaction:
                session.delete(transaction)
                session.commit()
                return True
            return False
        except SQLAlchemyError:
            session.rollback()
            return False
        finally:
            session.close()

    def update_transaction(self, transaction_id: int, user_id: int, **kwargs) -> Optional[Transaction]:
        """Update a transaction"""
        try:
            session = self.Session()
            transaction = session.query(Transaction).filter(
                Transaction.id == transaction_id,
                Transaction.user_id == user_id
            ).first()
            
            if transaction:
                for key, value in kwargs.items():
                    if hasattr(transaction, key):
                        setattr(transaction, key, value)
                session.commit()
                return transaction
            return None
        except SQLAlchemyError:
            session.rollback()
            return None
        finally:
            session.close() 