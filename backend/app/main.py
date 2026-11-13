# Backend FastAPI Application

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pathlib import Path

app = FastAPI()

# Allow all origins for development; adjust for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database URL – default to shared SQLite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///../shared/database.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Ensure the medicines table exists on startup
@app.on_event("startup")
def init_db():
    init_sql_path = Path(__file__).resolve().parents[2] / "shared" / "init.sql"
    if init_sql_path.exists():
        with engine.begin() as conn:
            conn.executescript(init_sql_path.read_text())

@app.get("/api/health")
async def health():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) AS cnt FROM medicines")).fetchone()
        count = result["cnt"] if result else 0
    return {"status": "healthy", "medicines_count": count}
