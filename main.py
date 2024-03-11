from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from api_app.db_manager import DbManager
from api_app import crud, models, schemas
from datetime import datetime, date

dbManager = DbManager()

app = FastAPI()

shapes = [
    {"item": "Circle", "number": 1, "id": 1},
    {"item": "Triangle", "number": 3, "id": 2},
    {"item": "Rectangle", "number": 4, "id": 3},
]

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}


@app.get("/shapes")
async def get_shapes():
    return shapes


@app.get("/shapes/{shape_id}")
async def get_shape_by_id(shape_id: int):
    # return [shape for shape in shapes if shape["id"] == shape_id]
    for shape in shapes:
        if shape["id"] == shape_id:
            return shape
    raise HTTPException(status_code=404, detail=f"No shape with id {shape_id} found")


def get_db():
    dbManager = DbManager()
    db = dbManager.SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Input Model = Request Body ['publisher'] == 'GreenWay , Output Model = Response Body == 'GreenWayBase'
@app.get("/greenway/records/{id}", response_model=schemas.GreenwayBase)
def read_greenway_record_by_id(id: int, db: Session = Depends(get_db)):
    gw_data = crud.get_greenway_first_record(db, id)
    if gw_data is None:
        raise HTTPException(status_code=404, detail=f"Record id {id} not found.")
    return gw_data


@app.get("/greenway/records/", response_model=list[schemas.GreenwayBase])
async def read_greenway_records_limit(
    skip: int = 0, limit: int = 50, db: Session = Depends(get_db)
):
    records = crud.get_greenway_items_with_limit(db, skip=skip, limit=limit)
    return records

def read_greenway_by_time(
    from_date: datetime = date(2016,3,1), 
    to_date: datetime = date(2023, 12, 1),):
    
