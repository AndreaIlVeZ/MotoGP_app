from fastapi import APIRouter, HTTPException, Depends
from app.backend import models, schemas
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.backend.db import get_db

## define the specific rider router
rider_router = APIRouter(prefix ="/riders", tags=["Riders"])


#list all riders ( maybe for a standard query)
@rider_router.get("/",  response_model=schemas.RidersList)
# riders depends on the db and i tell it to do a nice all query
# the glue!!!
def list_riders(db: Session = Depends(get_db)):
    riders = db.query(models.Rider).all()
    return riders

@rider_router.get("/{rider_id}/stats", response_model=schemas.RiderWithResults)
def get_rider_stats(rider_id: int, db: Session = Depends(get_db)):
    # Step 1: Use MODEL to fetch rider
    rider = db.query(models.Rider).filter(models.Rider.id == rider_id).first()
    
    # Step 2: Use MODEL RELATIONSHIPS to fetch related data
    stats = db.query(
        func.count(models.ResultsRace.id),
        func.sum(models.ResultsRace.points),
        func.min(models.ResultsRace.position)
    ).filter(
        models.ResultsRace.rider_id == rider_id  # ← Using foreign key!
    ).first()
    
    # Step 3: MANUALLY construct the SCHEMA response
    return schemas.RiderWithResults(
        id=rider.id,
        name=rider.name,
        surname=rider.surname,
        nationality=rider.nationality,
        career_status=rider.career_status,
        total_races=stats[0] or 0,
        total_points=stats[1] or 0.0,
        best_position=stats[2]
    )