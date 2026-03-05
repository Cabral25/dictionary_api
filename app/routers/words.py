from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Word
from ..schemas import WordCreate, WordOut
from ..dependencies import get_db, admin_required, get_current_user


router = APIRouter(prefix='/words')


@router.get('/', response_model=list[WordOut])
def list_words(db: Session = Depends(get_db)):
    words = db.query(Word).all()


@router.post('/', dependencies=[Depends(admin_required)])
def create_word(word: WordCreate, db: Session = Depends(get_db)):
    word = ''