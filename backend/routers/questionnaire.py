# routers/questionnaire.py
# Endpoints pour le questionnaire comportemental

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.result import Result
from models.child import Child
from models.parent import Parent
from routers.child import get_current_parent
import json

router = APIRouter(prefix="/questionnaire", tags=["Questionnaire"])


def calculate_score(answers: dict) -> float:
    """
    Calcule un score de risque basé sur les réponses.
    Score entre 0.0 (aucun risque) et 1.0 (risque élevé)

    ⚠️ Version simplifiée pour le MVP
    P2 pourra remplacer cette logique par son vrai moteur IA
    """
    # Signaux de risque — si True = signe inquiétant
    risk_signals = [
        answers.get("pas_contact_visuel", False),
        answers.get("pas_reponse_prenom", False),
        answers.get("pas_de_pointage", False),
        answers.get("comportements_repetitifs", False),
        answers.get("retard_langage", False),
        answers.get("pas_imitation", False),
        answers.get("hypersensibilite", False),
    ]

    if not any(isinstance(v, bool) for v in risk_signals):
        return 0.2

    nb_signaux = sum(1 for s in risk_signals if s is True)
    score = nb_signaux / len(risk_signals)
    return round(score, 2)


def determine_risk_level(score: float) -> str:
    """Convertit le score en niveau de risque"""
    if score < 0.35:
        return "VERT"
    elif score < 0.60:
        return "ORANGE"
    else:
        return "ROUGE"


def get_message(risk_level: str) -> str:
    """Retourne un message empathique selon le niveau"""
    messages = {
        "VERT": "Le développement de votre enfant semble se dérouler normalement. Continuez les activités d'éveil quotidiennes.",
        "ORANGE": "Quelques points méritent attention. Une réévaluation dans 3 mois est recommandée.",
        "ROUGE": "Une consultation avec un spécialiste est recommandée. Vous faites déjà quelque chose d'important.",
    }
    return messages.get(risk_level, "Analyse terminée.")


@router.post("/{child_id}")
def submit_questionnaire(
    child_id: int,
    answers: dict,
    current_parent: Parent = Depends(get_current_parent),
    db: Session = Depends(get_db),
):
    """
    POST /questionnaire/{child_id}
    Reçoit les réponses au questionnaire et calcule le score
    """

    # 1. Vérifier que l'enfant appartient au parent connecté
    child = (
        db.query(Child)
        .filter(Child.id == child_id, Child.parent_id == current_parent.id)
        .first()
    )

    if not child:
        raise HTTPException(status_code=404, detail="Enfant introuvable")

    # 2. Calculer le score
    score = calculate_score(answers)
    risk_level = determine_risk_level(score)
    message = get_message(risk_level)

    # 3. Sauvegarder le résultat en base de données
    result = Result(
        child_id=child_id,
        questionnaire_answers=json.dumps(answers),
        score_questionnaire=score,
        score_final=score,
        risk_level=risk_level,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    # 4. Retourner les résultats
    return {
        "result_id": result.id,
        "child_name": child.first_name,
        "score_final": score,
        "risk_level": risk_level,
        "message": message,
    }


@router.get("/{child_id}/results")
def get_child_results(
    child_id: int,
    current_parent: Parent = Depends(get_current_parent),
    db: Session = Depends(get_db),
):
    """
    GET /questionnaire/{child_id}/results
    Récupère tous les résultats d'un enfant
    """

    # Vérifier que l'enfant appartient au parent connecté
    child = (
        db.query(Child)
        .filter(Child.id == child_id, Child.parent_id == current_parent.id)
        .first()
    )

    if not child:
        raise HTTPException(status_code=404, detail="Enfant introuvable")

    # Récupérer tous les résultats
    results = db.query(Result).filter(Result.child_id == child_id).all()

    return {
        "child_name": child.first_name,
        "total_evaluations": len(results),
        "results": [
            {
                "result_id": r.id,
                "score_final": r.score_final,
                "risk_level": r.risk_level,
                "date": r.created_at,
            }
            for r in results
        ],
    }
