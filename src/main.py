import clusters
import settings
import profiles

from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

import models
from database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(clusters.routers.router)
app.include_router(settings.routers.router)
app.include_router(profiles.routers.router)


