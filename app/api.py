from pathlib import Path
import numpy as np
from fastapi import FastAPI, Response, Depends
from joblib import load
from .schemas import Wine, Rating, feature_names
from sqlalchemy.orm import Session, sessionmaker
from .database import SessionLocal, engine, Base
from .models import User
import os
from sqlalchemy import create_engine


DATABASE_URL = os.environ.get("DATABASE_URL")   # ★ 이게 환경변수 읽는 코드야!

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

ROOT_DIR = Path(__file__).parent.parent

app = FastAPI()
scaler = load(ROOT_DIR / "artifacts/scaler.joblib")
model = load(ROOT_DIR / "artifacts/model.joblib")


@app.get("/")
def root():
    return "Wine Quality Ratings"

# response_model : target
# sample : Feature
@app.post("/predict", response_model=Rating)
def predict(response: Response, sample: Wine):
    sample_dict = sample.dict()
    features = np.array([sample_dict[f] for f in feature_names]).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)[0]
    response.headers["X-model-score"] = str(prediction)
    return Rating(quality=prediction)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.get("/users")
def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    return users

@app.get("/dbtest")
def db_test():
    db = SessionLocal()
    result = db.execute("SELECT 1;").fetchone()
    db.close()
    return {"db_ok": result[0] == 1}