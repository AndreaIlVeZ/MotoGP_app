
"""
schemas is the physical instance for the app to define the smallest component to 
get the data needed, to be then used in the other layery. 
This is not to be confused with the models in the models.py files, 
which define the database structure and relationships.

This is a nice example of impedence mismatch solution, where the database models 
may contain more information than what is needed for specific operations,

e.g. : rider_motogp could be a class with multiple fields, but coming from different
database tables, for example anagraphic data from the Rider table, team data from the Team table,
and performance data from the RaceResult table.
"""

from datetime import date as date_type
from pydantic import BaseModel , ConfigDict


class RiderBase(BaseModel):

    id: int
    name: str
    surname: str
    nationality: str | None = None
    career_status: str | None = None

    model_config = ConfigDict(from_attributes=True)




class RidersList(BaseModel):
    """Schema for listing riders (minimal info)"""
    id: int
    name: str
    surname: str
    nationality: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


# Season Schemas (Read-only)
class SeasonResponse(BaseModel):
    """Schema for returning season data"""
    id: int
    year: int
    category: str
    
    model_config = ConfigDict(from_attributes=True)


# RaceCircuit Schemas (Read-only)
class RaceCircuitResponse(BaseModel):
    """Schema for returning race circuit data"""
    id: int
    season_id: int
    circuit: str | None = None
    date: date_type | None = None
    
    model_config = ConfigDict(from_attributes=True)


# ResultsRace Schemas (Read-only)
class ResultsRaceResponse(BaseModel):
    """Schema for returning race results"""
    id: int
    rider_id: int
    race_circuit_id: int
    position: int | None = None
    points: float | None = None
    
    model_config = ConfigDict(from_attributes=True)


# Combined/Enriched Schemas (Your "impedance mismatch" example)
class RiderWithResults(BaseModel):
    """
    Enriched rider data combining multiple tables.
    Example of solving impedance mismatch - data from Rider + ResultsRace tables.
    """
    id: int
    name: str
    surname: str
    nationality: str | None = None
    career_status: str | None = None
    total_races: int = 0
    total_points: float = 0.0
    best_position: int | None = None
    
    model_config = ConfigDict(from_attributes=True)


class RaceWithResults(BaseModel):
    """
    Race circuit with all results.
    Combines RaceCircuit + ResultsRace + Rider data.
    """
    id: int
    circuit: str | None = None
    date: date_type | None = None
    season_year: int
    category: str
    # Could include list of results here if needed
    
    model_config = ConfigDict(from_attributes=True)