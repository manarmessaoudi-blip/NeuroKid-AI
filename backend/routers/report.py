# Endpoint pour générer et télécharger le rapport PDF

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
from models.result import Result
from models.child import Child
from models.parent import Parent
from routers.child import get_current_parent
from services.pdf_generator import generate_pdf
import os

router = APIRouter(prefix="/report", tags=["Rapport PDF"])


@router.get("/{result_id}")
def download_report(
    result_id: int,
    current_parent: Parent = Depends(get_current_parent),
    db: Session = Depends(get_db),
):
    """
    GET /report/{result_id}
    Génère et télécharge le rapport PDF
    """

    # 1. Récupérer le résultat
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Résultat introuvable")

    # 2. Vérifier les droits d'accès
    child = (
        db.query(Child)
        .filter(Child.id == result.child_id, Child.parent_id == current_parent.id)
        .first()
    )
    if not child:
        raise HTTPException(status_code=403, detail="Accès interdit")

    # 3. Générer le PDF
    pdf_path = generate_pdf(result, child, current_parent)

    # 4. Vérifier que le fichier existe
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=500, detail="Erreur génération PDF")

    # 5. Retourner le fichier PDF
    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"neurokid_{child.first_name}_{result_id}.pdf",
    )
