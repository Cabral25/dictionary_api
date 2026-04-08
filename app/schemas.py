from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=25)
    is_admin: bool = False


class UserCreateOut(BaseModel):
    username: str
    email: str
    is_admin: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class WordCreate(BaseModel):
    word: str
    meaning: str
    example: str = None


class WordUpdate(BaseModel):
    word: str
    meaning: str
    example: str = None


class WordOut(BaseModel):
    word_id: int
    word: str
    meaning: str

    class DictConfig:
        """What does this do?"""
        from_attributes = True