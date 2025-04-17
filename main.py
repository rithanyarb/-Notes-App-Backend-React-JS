from fastapi import FastAPI
from database import engine
import models
from routers import auth, notes, user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(user.router)