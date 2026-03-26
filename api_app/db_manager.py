import sys
import os
# Add the project root to sys.path so the 'config' module is visible when the script is run directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
from typing import Any, List
from sqlalchemy import column, select, insert, text, delete
from sqlalchemy import create_engine, Table, MetaData, inspect
from sqlalchemy.orm import Session, sessionmaker

from api_app.models import Base

c = Config()


class DbManager:
    def __init__(self, use_local=False) -> None:
        uri = c.LOCAL_DATABASE_URI if use_local else c.SQLALCHEMY_DATABASE_URI
        self.engine = create_engine(uri)
        self.SessionLocal = sessionmaker(self.engine)

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)
        print("Initialization - Tables created successfully if they didn't exist.")

    def connect_with_existing_table(self, table_name: str):
        metadata = MetaData()
        return Table(table_name, metadata, autoload_with=self.engine)

    def reset_tables(self, table_name=None):
        if table_name:
            table = Base.metadata.tables.get(table_name)
            if table is not None:
                table.drop(self.engine)
                table.create(self.engine)
                print(f"Resetting table {table_name} - Done!")
            else:
                print(f"Table '{table_name}' not found in declarative metadata.")
        else:
            Base.metadata.drop_all(self.engine)
            self.create_tables()
            print("Resetting all tables - Done!")

    def truncate_tables(self, table_name=None):
        with self.engine.begin() as conn:
            if table_name:
                table = Base.metadata.tables.get(table_name)
                if table is not None:
                    conn.execute(delete(table))
                    print(f"Truncated data inside table '{table_name}'.")
                else:
                    print(f"Table '{table_name}' not found in metadata.")
            else:
                for table in reversed(Base.metadata.sorted_tables):
                    conn.execute(delete(table))
                print("Truncated data inside all tables.")

    def check_health(self) -> bool:
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database health check passed. Connection successful.")
            return True
        except Exception as e:
            print(f"Database health check failed: {e}")
            return False

    def get_all_table_names(self) -> List:
        inspector = inspect(self.engine)
        return inspector.get_table_names()
    
    def get_engine(self):
        return self.engine

    def insert_batch(self, table_name, data: list):
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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store_true', help='Use local SQLite database')
    args = parser.parse_args()
    
    try:
        db = DbManager(use_local=args.local)
        if db.check_health():
            print("Successfully connected to the database!")
    except Exception as e:
        print("Failed to connect or initialize the database.")
        print(f"Error details: {e}")
