# Endpoints inscription et connexion

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.parent import Parent
from schemas import ParentCreate, ParentLogin, Token
from services.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register", response_model=Token)
def register(data: ParentCreate, db: Session = Depends(get_db)):
    """
    POST /auth/register
    Crée un nouveau compte parent
    """
    # 1. Vérifier si l'email existe déjà
    existing = db.query(Parent).filter(Parent.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé"
        )

    # 2. Hacher le mot de passe
    hashed_pw = hash_password(data.password)

    # 3. Créer le parent dans la base de données
    new_parent = Parent(
        email=data.email,
        hashed_password=hashed_pw,
        full_name=data.full_name
    )
    db.add(new_parent)
    db.commit()
    db.refresh(new_parent)

    # 4. Retourner un token JWT
    token = create_access_token(data={"sub": new_parent.email})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(data: ParentLogin, db: Session = Depends(get_db)):
    """
    POST /auth/login
    Connecte un parent existant
    """
    # 1. Chercher le parent par email
    parent = db.query(Parent).filter(Parent.email == data.email).first()

    # 2. Vérifier email + mot de passe
    if not parent or not verify_password(data.password, parent.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )

    # 3. Retourner le token
    token = create_access_token(data={"sub": parent.email})
    return {"access_token": token, "token_type": "bearer"}