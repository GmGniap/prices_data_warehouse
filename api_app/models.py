from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column

from datetime import datetime


class Base(DeclarativeBase):
    pass


class GreenWay(Base):
    __tablename__ = "greenway_db"
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


class SummaryInfo(Base):
    __tablename__ = "summary"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dataset_name: Mapped[str] = mapped_column(String, nullable=False)
    scraped_date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String, nullable=False)
    total_rows: Mapped[int] = mapped_column(Integer, nullable=True)
    total_cols: Mapped[int] = mapped_column(Integer, nullable=True)
    last_scraped_url: Mapped[str] = mapped_column(String, nullable=True)