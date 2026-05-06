from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

# Importer tous les modèles pour créer les tables
import models
from routers import auth 

# Créer toutes les tables dans neurokid.db au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NeuroKid AI — Backend API",
    description="API pour le dépistage précoce de troubles du développement",
    version="1.0.0"
)

# Autoriser le frontend React (port 3000) à parler au backend (port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)  

@app.get("/")
def root():
    return {"message": "NeuroKid AI est en ligne 🧠"}