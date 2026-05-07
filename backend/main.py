from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import auth, child, questionnaire, video, report

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NeuroKid AI — Backend API",
    description="API pour le dépistage précoce de troubles du développement",
    version="1.0.0",
)

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
    return {"message": "NeuroKid AI est en ligne 🧠"}
