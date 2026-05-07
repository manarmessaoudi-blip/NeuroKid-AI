# Vérifications de sécurité supplémentaires

import os

# Extensions vidéo autorisées
ALLOWED_VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

# Taille maximale vidéo : 50 MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024


def is_valid_video(filename: str, file_size: int) -> tuple[bool, str]:
    """
    Vérifie qu'un fichier vidéo est valide et sécurisé.
    Retourne (True, "") si valide, (False, "message erreur") sinon.
    """
    # Vérifier l'extension
    extension = filename.split(".")[-1].lower()
    if extension not in ALLOWED_VIDEO_EXTENSIONS:
        return False, f"Format non autorisé. Utilisez : {ALLOWED_VIDEO_EXTENSIONS}"

    # Vérifier la taille
    if file_size > MAX_VIDEO_SIZE:
        return False, "Vidéo trop volumineuse. Maximum 50 MB."

    return True, ""


def anonymize_child_data(child_data: dict) -> dict:
    """
    Anonymise les données d'un enfant pour les logs.
    Ne jamais logger des données sensibles en clair !
    """
    return {
        "id": child_data.get("id"),
        "age_months": child_data.get("age_months"),
        "gender": child_data.get("gender"),
        # Prénom remplacé par les initiales
        "initial": child_data.get("first_name", "?")[0].upper(),
    }


def secure_delete_file(file_path: str) -> bool:
    """
    Supprime un fichier de façon sécurisée.
    Retourne True si supprimé, False si erreur.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception:
        return False
