from fastapi import APIRouter, Depends
### mi serve il reference degli schemi 
from app.backend import schemas, models
## mi serve il model reference
## sto andando ad operare funzioni su db, quindi mi serve sqlalchemy

from sqlalchemy.orm import Session
from sqlalchemy import func
# mi serve la connessione del db, per creare la sessione e quindi la query
from app.backend.db import get_db


## definisco il router per race

race_router = APIRouter(prefix = "/races")

## definisco gli endpoint con le relative funzinoi

race_router.get("", response_model=schemas.RaceWithResults)
def list_races_results(db: Session = Depends(get_db)):
    # Query
    races = db.query(models.RaceCircuit).all()
    return races
