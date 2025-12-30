from fastapi import FastAPI
from . import database
from . import models
from .api import auth, user

app=FastAPI(title="Session Based Auth System")
Basee=database.Base

Basee.metadata.create_all(bind=database.engine)

app.include_router(auth.router)
app.include_router(user.router)
