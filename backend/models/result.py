# Table des résultats d'analyse

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"))

    # Réponses au questionnaire (stockées en JSON)
    questionnaire_answers = Column(String)

    # Vidéo
    video_path = Column(String, nullable=True)
    video_analyzed = Column(Boolean, default=False)

    # Scores
    score_questionnaire = Column(Float, nullable=True)
    score_video = Column(Float, nullable=True)
    score_final = Column(Float, nullable=True)
    risk_level = Column(String, nullable=True)  # "VERT", "ORANGE", "ROUGE"

    # Rapport PDF
    pdf_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("Child", back_populates="results")