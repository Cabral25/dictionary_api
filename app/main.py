from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app.routers import users, words
import logging

Base.metadata.create_all(bind=engine)


app = FastAPI()

logger = logging.getLogger('uvicorn.error')


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    "Captura erros de validação do pydantic."
    logger.warning('Validation error: %s', exc)
    return JSONResponse(
        status_code=422,
        content={'detail': 'Invalid request data'},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Captura qualquer erro não tratado. Ativa quando algo quebra no código
       que não foi explicitamente tratado."""
    logger.exception('Unhandled exception: %s', exc)
    return JSONResponse(
        status_code=500,
        content={'detail': 'Internal server error'},
    )


app.include_router(users.router)
app.include_router(words.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8003'], # adicionar uma origem válida mais tarde
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)