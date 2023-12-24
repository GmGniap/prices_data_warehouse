from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from db_manager import DbManager
from api_app import crud, models, schemas

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
    db = dbManager.SessionLocal
    try:
        yield db
    finally:
        db.close()


@app.get("/greenway/{id}", response_model=schemas.GreenwayBase)
def read_greenway(id: int, db: Session = Depends(get_db)):
    gw_data = crud.get_greenway_first_record(db, id)
    if gw_data is None:
        raise HTTPException(status_code=404, detail=f"Record id {id} not found.")
    return gw_data
