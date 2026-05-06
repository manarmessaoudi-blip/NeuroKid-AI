# Format des données que l'API reçoit et envoie

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ParentCreate(BaseModel):
    """Données pour créer un compte — envoyées par le frontend"""
    email: EmailStr
    password: str
    full_name: str


class ParentLogin(BaseModel):
    """Données pour se connecter"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Réponse après connexion réussie"""
    access_token: str
    token_type: str


class ChildCreate(BaseModel):
    """Données pour créer un profil enfant"""
    first_name: str
    age_months: int
    gender: str
    language: Optional[str] = "fr"


class ChildResponse(BaseModel):
    """Réponse quand on retourne un profil enfant"""
    id: int
    first_name: str
    age_months: int
    gender: str
    language: str

    class Config:
        from_attributes = True


class ResultResponse(BaseModel):
    """Réponse après une analyse"""
    id: int
    child_id: int
    score_final: Optional[float]
    risk_level: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True