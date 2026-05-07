from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine, Base
import models
from routers import auth, child, questionnaire, video, report

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NeuroKid AI — Backend API",
    description="API pour le dépistage précoce de troubles du développement",
    version="1.0.0",
)

# Limite la taille des fichiers uploadés pour la securite
# Maximum 50 MB pour les vidéos
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50 MB en bytes


@app.middleware("http")
async def limit_upload_size(request: Request, call_next):
    """Bloque les fichiers trop volumineux avant même de les traiter"""
    if request.method == "POST":
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_UPLOAD_SIZE:
            return JSONResponse(
                status_code=413,
                content={"detail": "Fichier trop volumineux. Maximum 50 MB."},
            )
    return await call_next(request)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(child.router)
app.include_router(questionnaire.router)
app.include_router(video.router)
app.include_router(report.router)


@app.get("/")
def root():
    return {
        "message": "NeuroKid AI est en ligne 🧠",
        "version": "1.0.0",
        "docs": "/docs",
    }
