from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/inventario", tags=["Inventario"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.InventarioResponse)
def crear_item(item: schemas.InventarioCreate, db: Session = Depends(get_db)):
    nuevo = models.Inventario(**item.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[schemas.InventarioResponse])
def listar_items(db: Session = Depends(get_db)):
    return db.query(models.Inventario).all()
