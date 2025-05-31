from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/permissions", tags=["Permissions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Permission)
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    db_permission = models.Permission(name=permission.name)
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

@router.get("/", response_model=list[schemas.Permission])
def get_permissions(db: Session = Depends(get_db)):
    return db.query(models.Permission).all()

@router.get("/{permission_id}", response_model=schemas.Permission)
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(models.Permission).get(permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

@router.put("/{permission_id}", response_model=schemas.Permission)
def update_permission(permission_id: int, permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    db_permission = db.query(models.Permission).get(permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db_permission.name = permission.name
    db.commit()
    db.refresh(db_permission)
    return db_permission

@router.delete("/{permission_id}")
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = db.query(models.Permission).get(permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(db_permission)
    db.commit()
    return {"detail": "Permission deleted"}