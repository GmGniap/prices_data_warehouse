import sys
import os
# Add the project root to sys.path so the 'config' module is visible when the script is run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
from typing import Any, List
from sqlalchemy import column, select, insert, text
from sqlalchemy import create_engine, Table, MetaData, inspect
from sqlalchemy.orm import Session, sessionmaker

from api_app.models import Base

c = Config()


class DbManager:
    def __init__(self) -> None:
        self.engine = create_engine(c.SQLALCHEMY_DATABASE_URI)
        self.SessionLocal = sessionmaker(self.engine)
        self.create_tables()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def connect_with_existing_table(self, table_name: str):
        metadata = MetaData()
        return Table(table_name, metadata, autoload_with=self.engine)

    def reset_tables(self):
        Base.metadata.drop_all(self.engine)
        self.create_tables()
        print("Resetting tables - Done!")

    def get_all_table_names(self) -> List:
        inspector = inspect(self.engine)
        return inspector.get_table_names()
    
    def get_engine(self):
        return self.engine

    def insert_batch(self, table_name, data: list):
        """
        table_name : Table name,
        data : List of dictionary
        """
        print(f"Inserting data into {table_name}...")
        table = self.connect_with_existing_table(table_name)
        with self.SessionLocal() as session:
            session.execute(
                insert(table),
                data,
            )
            session.commit()
        print(f"Insert done for {table_name}!")

if __name__ == "__main__":
    try:
        safe_uri = c.SQLALCHEMY_DATABASE_URI.split('@')[-1] if '@' in c.SQLALCHEMY_DATABASE_URI else c.SQLALCHEMY_DATABASE_URI
        print(f"Attempting to connect to the database engine: {safe_uri}")
        db = DbManager()
        with db.engine.connect() as connection:
            print("Successfully connected to the database and initialized tables!")
    except Exception as e:
        print("Failed to connect or initialize the database.")
        print(f"Error details: {e}")
