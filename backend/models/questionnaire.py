# Table des questions du questionnaire

from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)           # Le texte de la question
    category = Column(String)       # Ex: "langage", "contact_visuel", "social"
    weight = Column(Integer)        # Importance de la question (1 à 3)
    is_risk_if_true = Column(Boolean, default=True)  # True = répondre oui = signe de risque