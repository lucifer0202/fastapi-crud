from sqlalchemy.orm import Session
import models

def get_items(db: Session):
    return db.query(models.Item).all()

def create_item(db: Session, name: str, description: str):
    item = models.Item(name=name, description=description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
