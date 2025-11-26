from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.routers import auth, scenarios, games, players, decisions, scoreboard, artifacts

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cyber Tabletop API", version="1.0.0")

# CORS middleware
import os
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(scenarios.router, prefix="/scenarios", tags=["scenarios"])
app.include_router(games.router, prefix="/games", tags=["games"])
app.include_router(players.router, prefix="", tags=["players"])
app.include_router(decisions.router, prefix="/games", tags=["decisions"])
app.include_router(scoreboard.router, prefix="/games", tags=["scoreboard"])
app.include_router(artifacts.router, prefix="/artifacts", tags=["artifacts"])


@app.get("/")
def root():
    return {"message": "Cyber Tabletop API"}


@app.get("/health")
def health():
    return {"status": "healthy"}

