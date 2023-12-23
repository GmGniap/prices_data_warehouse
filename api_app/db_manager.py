from config import Config
from typing import Any
from sqlalchemy import column, select, insert, text
from sqlalchemy import create_engine, Table, MetaData
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
