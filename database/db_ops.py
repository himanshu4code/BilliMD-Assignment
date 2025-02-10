import os
from typing import Any, Type, TypeVar, Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from logger.blog_logger import setup_logger

T = TypeVar('T')

logger = setup_logger(__name__)

class DatabaseOperations:
    def __init__(self):
        connection_string = os.getenv("BLOG_DB_URL")
        if not connection_string:
            logger.error("Database URL not found in environment variables")
            raise ValueError("Database URL not found in environment variables")
        logger.info("Initializing database connection")
        self.engine = create_engine(connection_string)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = None

    def __enter__(self):
        self.db = self.SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            self.db.close()

    def create_record(self, model: Type[T], data: dict) -> Optional[T]:
        try:
            logger.info(f"Creating new record for model: {model.__name__}")
            db_item = model(**data)
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            logger.info(f"Successfully created {model.__name__} record")
            return db_item
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating record: {str(e)}")
            self.db.rollback()
            raise Exception(f"Error creating record: {str(e)}")

    def get_record(self, model: Type[T], id: Any) -> Optional[T]:
        try:
            return self.db.query(model).filter(model.id == id).first()
        except SQLAlchemyError as e:
            raise Exception(f"Error retrieving record: {str(e)}")

    def get_all_records(self, model: Type[T], skip: int = 0, limit: int = 100) -> List[T]:
        try:
            return self.db.query(model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise Exception(f"Error retrieving records: {str(e)}")

    def update_record(self, model: Type[T], id: Any, data: dict) -> Optional[T]:
        try:
            db_item = self.db.query(model).filter(model.id == id).first()
            if db_item:
                for key, value in data.items():
                    setattr(db_item, key, value)
                self.db.commit()
                self.db.refresh(db_item)
            return db_item
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error updating record: {str(e)}")

    def delete_record(self, model: Type[T], id: Any) -> bool:
        try:
            db_item = self.db.query(model).filter(model.id == id).first()
            if db_item:
                self.db.delete(db_item)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error deleting record: {str(e)}")
