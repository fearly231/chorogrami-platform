from fastapi import FastAPI
from sqlmodel import Session

from api.router import api_router
from database.database import initialize_database, engine

from prometheus_fastapi_instrumentator import Instrumentator

with Session(engine) as session:
    initialize_database(session)

app = FastAPI()

Instrumentator().instrument(app).expose(app)  # Integrate Prometheus monitoring (DevOps)

app.include_router(api_router)
