from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserCreateOut(BaseModel):
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class WordCreate(BaseModel):
    word: str
    meaning: str


class WordUpdate(BaseModel):
    word: str
    meaning: str
    example: str


class WordOut(BaseModel):
    word_id: int
    word: str
    meaning: str

    class DictConfig:
        """What does this do?"""
        from_attributes = True