from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class WordCreate(BaseModel):
    word: str
    meaning: str


class WordOut(BaseModel):
    word_id: int
    word: str
    meaning: str

    class DictConfig:
        from_attributes = True