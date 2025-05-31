from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

router = APIRouter(prefix="/role-permissions", tags=["RolePermissions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.RolePermission)
def assign_permission_to_role(data: schemas.RolePermissionCreate, db: Session = Depends(get_db)):
    exists = db.query(models.RolePermission).filter_by(
        role_id=data.role_id,
        permission_id=data.permission_id
    ).first()
    if exists:
        raise HTTPException(status_code=400, detail="Permission already assigned to this role.")
    rp = models.RolePermission(**data.dict())
    db.add(rp)
    db.commit()
    db.refresh(rp)
    return rp

@router.get("/", response_model=list[schemas.RolePermission])
def list_role_permissions(db: Session = Depends(get_db)):
    return db.query(models.RolePermission).all()

@router.get("/{rp_id}", response_model=schemas.RolePermission)
def get_role_permission(rp_id: int, db: Session = Depends(get_db)):
    rp = db.query(models.RolePermission).get(rp_id)
    if not rp:
        raise HTTPException(status_code=404, detail="Not found")
    return rp

@router.put("/{rp_id}", response_model=schemas.RolePermission)
def update_role_permission(rp_id: int, data: schemas.RolePermissionCreate, db: Session = Depends(get_db)):
    rp = db.query(models.RolePermission).get(rp_id)
    if not rp:
        raise HTTPException(status_code=404, detail="Not found")
    rp.role_id = data.role_id
    rp.permission_id = data.permission_id
    db.commit()
    db.refresh(rp)
    return rp

@router.delete("/{rp_id}")
def delete_role_permission(rp_id: int, db: Session = Depends(get_db)):
    rp = db.query(models.RolePermission).get(rp_id)
    if not rp:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(rp)
    db.commit()
    return {"detail": "Deleted"}