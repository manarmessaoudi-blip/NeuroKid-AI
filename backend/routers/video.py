# Endpoint pour upload et analyse de vidéo

import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.result import Result
from models.child import Child
from models.parent import Parent
from routers.child import get_current_parent

router = APIRouter(prefix="/video", tags=["Vidéo"])

# Dossier où stocker les vidéos temporairement
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Formats vidéo autorisés
ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}


def analyze_video_mock(video_path: str) -> float:
    """
    ⚠️ Version simulée — à remplacer par le vrai module de P2
    Retourne un score vidéo fictif pour le MVP
    """
    return 0.45


@router.post("/{result_id}")
async def upload_video(
    result_id: int,
    video: UploadFile = File(...),
    current_parent: Parent = Depends(get_current_parent),
    db: Session = Depends(get_db),
):
    """
    POST /video/{result_id}
    Upload une vidéo et met à jour le score final
    """

    # 1. Récupérer le résultat existant
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Résultat introuvable")

    # 2. Vérifier que l'enfant appartient au parent connecté
    child = (
        db.query(Child)
        .filter(Child.id == result.child_id, Child.parent_id == current_parent.id)
        .first()
    )
    if not child:
        raise HTTPException(status_code=403, detail="Accès interdit")

    # 3. Vérifier le format de la vidéo
    extension = video.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Format non autorisé. Formats acceptés : {ALLOWED_EXTENSIONS}",
        )

    # 4. Sauvegarder la vidéo avec un nom unique
    unique_filename = f"{uuid.uuid4()}.{extension}"
    video_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(video_path, "wb") as f:
        content = await video.read()
        f.write(content)

    # 5. Analyser la vidéo (simulation pour MVP)
    score_video = analyze_video_mock(video_path)

    # 6. Combiner score questionnaire + score vidéo
    score_questionnaire = result.score_questionnaire or 0.5
    score_final = round((score_questionnaire * 0.6) + (score_video * 0.4), 2)

    # 7. Recalculer le niveau de risque
    if score_final < 0.35:
        risk_level = "VERT"
    elif score_final < 0.60:
        risk_level = "ORANGE"
    else:
        risk_level = "ROUGE"

    # 8. Mettre à jour le résultat en base de données
    result.video_path = video_path
    result.video_analyzed = True
    result.score_video = score_video
    result.score_final = score_final
    result.risk_level = risk_level
    db.commit()
    db.refresh(result)

    # 9. Supprimer la vidéo après analyse (sécurité/confidentialité)
    if os.path.exists(video_path):
        os.remove(video_path)
        result.video_path = "supprimée"
        db.commit()

    return {
        "result_id": result.id,
        "child_name": child.first_name,
        "score_questionnaire": score_questionnaire,
        "score_video": score_video,
        "score_final": score_final,
        "risk_level": risk_level,
        "video_status": "analysée et supprimée ✅",
    }
