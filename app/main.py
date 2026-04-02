from fastapi import FastAPI
from database import Base, engine
from routers import users, words

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(users.router)
app.include_router(words.router)

dic = {'detail': [{'type': 'string_type', 'loc': ['body', 'word'], 'msg': 'input', 'input': 2000}]}
print(dic['detail'][0]['msg'])