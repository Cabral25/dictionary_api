from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Word, User
from schemas import WordCreate, WordOut
from dependencies import get_db, admin_required, get_current_user


router = APIRouter(prefix='/words')


@router.get('/', response_model=list[WordOut], tags=['Words'], summary='Read a list of words')
def list_words(db: Session = Depends(get_db)):
    words = db.query(Word).all()
    return words


@router.post('/', dependencies=[Depends(admin_required)], tags=['Words'])
def create_word(word: WordCreate, db: Session = Depends(get_db), user: User = Depends(admin_required)):
    word = Word(
        word=word.word,
        meaning=word.meaning,
        created_by=user.user_id
    )
    db.add(word)
    db.commit()
    return {'msg': 'created'}


@router.patch('/words/{word_id}')
def edit_word(word_id: int):
    pass


@router.delete('/words/{word_id}')
def delete_word(word_id: int):
    pass