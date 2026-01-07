"""
Database loader for ETL pipeline.
Handles idempotent loading of race results into PostgreSQL.
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
import pandas as pd
from typing import Dict, Tuple
import logging

from app.backend.models import Rider, Season, RaceCircuit, ResultsRace

logger = logging.getLogger(__name__)


def load_results_to_db(df: pd.DataFrame, session: Session) -> Dict[str, int]:
    """
    Load race results to database with idempotency.
    
    Args:
        df: DataFrame with race results
        session: SQLAlchemy session
    
    Returns:
        Dictionary with counts of created/updated records
    """
    stats = {
        'riders_created': 0,
        'riders_updated': 0,
        'seasons_created': 0,
        'races_created': 0,
        'results_created': 0,
        'results_updated': 0,
    }
    
    try:
        logger.info(f"Processing {len(df)} race results...")
        
        # Step 1: Upsert Riders
        rider_map = _upsert_riders(df, session, stats)
        
        # Step 2: Upsert Seasons
        season_map = _upsert_seasons(df, session, stats)
        
        # Step 3: Upsert Race Circuits
        race_map = _upsert_race_circuits(df, session, season_map, stats)
        
        # Step 4: Upsert Race Results
        _upsert_race_results(df, session, rider_map, race_map, stats)
        
        session.commit()
        logger.info(f"ETL completed: {stats}")
        return stats
        
    except Exception as e:
        session.rollback()
        logger.error(f"ETL failed: {e}")
        raise


def _upsert_riders(
    df: pd.DataFrame, 
    session: Session, 
    stats: Dict
) -> Dict[Tuple[str, str], int]:
    """Upsert riders and return mapping of (name, surname) -> rider_id"""
    rider_map = {}
    unique_riders = df[['rider_name', 'rider_surname', 'nationality']].drop_duplicates()
    
    for _, row in unique_riders.iterrows():
        name = row['rider_name']
        surname = row['rider_surname']
        nationality = row.get('nationality')
        
        rider = session.query(Rider).filter(
            and_(Rider.name == name, Rider.surname == surname)
        ).first()
        
        if rider:
            if nationality and rider.nationality != nationality:
                rider.nationality = nationality
                stats['riders_updated'] += 1
        else:
            rider = Rider(name=name, surname=surname, nationality=nationality)
            session.add(rider)
            session.flush()
            stats['riders_created'] += 1
            logger.debug(f"Created rider: {name} {surname}")
        
        rider_map[(name, surname)] = rider.id
    
    return rider_map


def _upsert_seasons(
    df: pd.DataFrame, 
    session: Session, 
    stats: Dict
) -> Dict[Tuple[int, str], int]:
    """Upsert seasons and return mapping of (year, category) -> season_id"""
    season_map = {}
    unique_seasons = df[['season_year', 'category']].drop_duplicates()
    
    for _, row in unique_seasons.iterrows():
        year = int(row['season_year'])
        category = row['category']
        
        season = session.query(Season).filter(
            and_(Season.year == year, Season.category == category)
        ).first()
        
        if not season:
            season = Season(year=year, category=category)
            session.add(season)
            session.flush()
            stats['seasons_created'] += 1
            logger.debug(f"Created season: {year} {category}")
        
        season_map[(year, category)] = season.id
    
    return season_map


def _upsert_race_circuits(
    df: pd.DataFrame, 
    session: Session, 
    season_map: Dict[Tuple[int, str], int],
    stats: Dict
) -> Dict[Tuple[int, str, str], int]:
    """Upsert race circuits and return mapping"""
    race_map = {}
    unique_races = df[['season_year', 'category', 'circuit', 'date']].drop_duplicates()
    
    for _, row in unique_races.iterrows():
        year = int(row['season_year'])
        category = row['category']
        circuit = row['circuit']
        date = pd.to_datetime(row['date']).date() if pd.notna(row['date']) else None
        
        season_id = season_map[(year, category)]
        
        race = session.query(RaceCircuit).filter(
            and_(
                RaceCircuit.season_id == season_id,
                RaceCircuit.circuit == circuit,
                RaceCircuit.date == date
            )
        ).first()
        
        if not race:
            race = RaceCircuit(season_id=season_id, circuit=circuit, date=date)
            session.add(race)
            session.flush()
            stats['races_created'] += 1
            logger.debug(f"Created race: {circuit} on {date}")
        
        race_map[(season_id, circuit, str(date))] = race.id
    
    return race_map


def _upsert_race_results(
    df: pd.DataFrame,
    session: Session,
    rider_map: Dict[Tuple[str, str], int],
    race_map: Dict[Tuple[int, str, str], int],
    stats: Dict
) -> None:
    """Upsert race results"""
    for _, row in df.iterrows():
        rider_id = rider_map[(row['rider_name'], row['rider_surname'])]
        
        year = int(row['season_year'])
        category = row['category']
        circuit = row['circuit']
        date = str(pd.to_datetime(row['date']).date() if pd.notna(row['date']) else None)
        
        # Find season_id first
        season_query = session.query(Season.id).filter(
            and_(Season.year == year, Season.category == category)
        ).first()
        season_id = season_query[0]
        
        race_circuit_id = race_map[(season_id, circuit, date)]
        
        position = int(row['position']) if pd.notna(row['position']) else None
        points = float(row['points']) if pd.notna(row['points']) else None
        
        result = session.query(ResultsRace).filter(
            and_(
                ResultsRace.rider_id == rider_id,
                ResultsRace.race_circuit_id == race_circuit_id
            )
        ).first()
        
        if result:
            if result.position != position or result.points != points:
                result.position = position
                result.points = points
                stats['results_updated'] += 1
        else:
            result = ResultsRace(
                rider_id=rider_id,
                race_circuit_id=race_circuit_id,
                position=position,
                points=points
            )
            session.add(result)
            stats['results_created'] += 1