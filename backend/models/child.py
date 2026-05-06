# models/child.py
# Table des enfants

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("parents.id"))
    first_name = Column(String)
    age_months = Column(Integer)
    gender = Column(String)
    language = Column(String, default="fr")

    # Relations
    parent = relationship("Parent", back_populates="children")
    results = relationship("Result", back_populates="child")