from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import users, words

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(users.router)
app.include_router(words.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], # adicionar uma origem válida mais tarde
    allow_credentials=True,
    allow_methos=['*'],
    allow_headers=['*'],
)