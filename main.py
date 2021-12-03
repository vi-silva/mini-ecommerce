from fastapi import FastAPI
from app.api.router import router
from app.models.models import Base
from app.db.db import engine

# Base.metadata.create_all(engine) #- o alembic faz isso agora

app = FastAPI()

app.include_router(router)