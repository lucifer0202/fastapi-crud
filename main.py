from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import crud, models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    return crud.get_items(db)

@app.post("/items/")
def create_item(name: str, description: str, db: Session = Depends(get_db)):
    return crud.create_item(db, name, description)

@app.put("/items/{item_id}")
async def update_item(item_id: int, name: str, description: str):
    db = SessionLocal()
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db_item.name = name
    db_item.description = description
    db.commit()
    return db_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}

