from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

from datetime import datetime
from constants import GREENWAY_DB, WISARRA_DB

class Base(DeclarativeBase):
    pass

class GreenWay(Base):
    __tablename__ = GREENWAY_DB
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime)
    crop: Mapped[str] = mapped_column(String, nullable=False)
    crop_id: Mapped[int] = mapped_column(Integer, nullable=False)
    crop_location: Mapped[str] = mapped_column(String, nullable=True)
    crop_name: Mapped[str] = mapped_column(String, nullable=True)
    market: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[str] = mapped_column(String, nullable=True)
    remark: Mapped[str] = mapped_column(String, nullable=True)
    state_id: Mapped[int]
    tab_date: Mapped[str] = mapped_column(String, nullable=True)
    tab_name: Mapped[str] = mapped_column(String, nullable=True)
    township: Mapped[str] = mapped_column(String, nullable=True)
    township_id: Mapped[int]
    unit: Mapped[str] = mapped_column(String, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime)

    def __str__(self):
        return f"{self.id}:{self.crop}-{self.price}"
    
    def convert_dict(self):
        return self.__dict__


class SummaryInfo(Base):
    __tablename__ = "summary"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dataset_name: Mapped[str] = mapped_column(String, nullable=False)
    scraped_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String, nullable=False)
    total_rows: Mapped[int] = mapped_column(Integer, nullable=True)
    total_cols: Mapped[int] = mapped_column(Integer, nullable=True)
    last_scraped_url: Mapped[str] = mapped_column(String, nullable=True)


class Wisarra(Base):
    __tablename__ = WISARRA_DB
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str]
    location: Mapped[str]
    marketplace: Mapped[str]
    min_price: Mapped[int] = mapped_column(Integer, nullable=True)
    max_price: Mapped[int] = mapped_column(Integer, nullable=True)
    currency: Mapped[str]
    quantity: Mapped[float]
    unit: Mapped[str]
    page_date : Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    ## Ref - https://stackoverflow.com/questions/10467199/the-pythonic-way-to-handle-sqlalchemy-models?rq=4
    @classmethod
    def get_by_id(cls, dbsession, filter_id):
        return dbsession.query(cls).filter(cls.id == filter_id).scalar()
