from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.models import Word, User
from app.schemas import WordCreate, WordOut, WordUpdate
from app.dependencies import get_db, admin_required
from app.rate_limit import rate_limiter


router = APIRouter(prefix='/words')


@router.get(
    '/list_words/',
    response_model=List[WordOut],
    tags=['Words'],
    summary='Read a list of words',
    dependencies=[Depends(rate_limiter)]
)
def list_words(page: int = Query(1, gt=0), db: Session = Depends(get_db)):
    limit = 5
    offset = (page - 1) * limit
    words = db.query(Word).order_by(Word.word_id).offset(offset).limit(limit).all()
    return words


@router.post('/create_word/', tags=['Words'], status_code=status.HTTP_201_CREATED)
def create_word(word: WordCreate, db: Session = Depends(get_db), user: User = Depends(admin_required)):
    word = Word(
        word=word.word,
        meaning=word.meaning,
        created_by=user.user_id
    )
    db.add(word)
    db.commit()
    return {'msg': 'created', 'word_id': {word.word_id}}


@router.patch('/edit/{word_id}', dependencies=[Depends(admin_required)], tags=['Words'])
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


@router.delete('/delete/{word_id}', dependencies=[Depends(admin_required)], tags=['Words'], status_code=status.HTTP_204_NO_CONTENT)
def delete_word(word_id: int, db: Session = Depends(get_db)):
    """Delete a word"""
    word = db.query(Word).filter(Word.word_id == word_id).first()

    if not word:
        raise HTTPException(status_code=404, detail='Word not found')

    db.delete(word)
    db.commit()
    return {'msg': f'The word {word.word} was deleted'}