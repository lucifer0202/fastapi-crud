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
