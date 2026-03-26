from fastapi import FastAPI
from database import Base, engine
from routers import users, words

Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(users.router)
app.include_router(words.router)


def a():

    def b(number: int):
        return number
    
    return b

res = a()
print(res(6))
print(a()(7))
res2 = a()(8)
print(res2)