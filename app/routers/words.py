from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List
from sqlalchemy.orm import Session
from models import Word, User
from schemas import WordCreate, WordOut, WordUpdate
from dependencies import get_db, admin_required, get_current_user
from rate_limit import rate_limiter


router = APIRouter(prefix='/words')


@router.get(
    '/',
    response_model=List[WordOut],
    tags=['Words'],
    summary='Read a list of words',
    dependencies=[Depends(rate_limiter), Depends(get_current_user)]
)
def list_words(page: int = Query(1, gt=0), db: Session = Depends(get_db)):
    limit = 2
    offset = (page - 1) * limit
    words = db.query(Word).offset(offset).limit(limit).all()
    return words


@router.post('/', tags=['Words'])
def create_word(word: WordCreate, db: Session = Depends(get_db), user: User = Depends(admin_required)):
    word = Word(
        word=word.word,
        meaning=word.meaning,
        created_by=user.user_id
    )
    db.add(word)
    db.commit()
    return {'msg': 'created'}


@router.patch('/words/{word_id}', dependencies=[Depends(admin_required)], tags=['Words'])
def edit_word(word_id: int, word_data: WordUpdate, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.word_id == word_id).first()

    if not word:
        raise HTTPException(status_code=404, detail='Word not found')

    word_update = word_data.model_dump()

    for key, value in word_update.items():
        setattr(word, key, value)

    db.commit()
    db.refresh(word)
    return word


@router.delete('/words/{word_id}', dependencies=[Depends(admin_required)], tags=['Words'])
def delete_word(word_id: int, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.word_id == word_id).first()

    if not word:
        raise HTTPException(status_code=404, detail='Word not found')

    db.delete(word)
    db.commit()
    return {'msg': f'The word {word.word} was deleted'}