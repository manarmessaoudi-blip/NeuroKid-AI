# routers/child.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.child import Child
from models.parent import Parent
from schemas import ChildCreate, ChildResponse
from services.security import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

router = APIRouter(prefix="/children", tags=["Enfants"])
security = HTTPBearer()


def get_current_parent(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Parent:
    token = credentials.credentials
    email = decode_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide ou expiré"
        )
    parent = db.query(Parent).filter(Parent.email == email).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return parent


@router.post("/", response_model=ChildResponse)
def create_child(
    data: ChildCreate,
    current_parent: Parent = Depends(get_current_parent),
    db: Session = Depends(get_db),
):
    new_child = Child(
        parent_id=current_parent.id,
        first_name=data.first_name,
        age_months=data.age_months,
        gender=data.gender,
        language=data.language,
    )
    db.add(new_child)
    db.commit()
    db.refresh(new_child)
    return new_child


@router.get("/", response_model=List[ChildResponse])
def get_my_children(
    current_parent: Parent = Depends(get_current_parent), db: Session = Depends(get_db)
):
    children = db.query(Child).filter(Child.parent_id == current_parent.id).all()
    return children


@router.get("/{child_id}", response_model=ChildResponse)
def get_child(
    child_id: int,
    current_parent: Parent = Depends(get_current_parent),
    db: Session = Depends(get_db),
):
    child = (
        db.query(Child)
        .filter(Child.id == child_id, Child.parent_id == current_parent.id)
        .first()
    )
    if not child:
        raise HTTPException(status_code=404, detail="Enfant introuvable")
    return child
