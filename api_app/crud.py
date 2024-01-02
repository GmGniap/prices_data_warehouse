from sqlalchemy.orm import Session
from api_app import models, schemas


def get_greenway_first_record(db: Session, id: int):
    return db.query(models.GreenWay).filter(models.GreenWay.id == id).first()


def get_greenway_items_with_limit(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.GreenWay).offset(skip).limit(limit).all()


def get_greenway_by_date(db: Session, from_date, to_date):
    pass
