"""
This is the physical instance for the database and the models
atm we do not have the data yêt, so this is just a placeholder file.
"""


from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.backend.db import Base

class Rider(Base):
    __tablename__ = "riders"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False )
    surname = Column(String, index=True, nullable=False )
    nationality = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    career_status = Column(String, nullable=True)

    # Relationships
    results = relationship("ResultsRace", back_populates="rider")

class Season(Base):
    __tablename__ = "seasons"
    
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True, nullable=False, unique=True)
    category = Column(String, index=True, nullable=False)
    
    # Relationship to race circuits
    race_circuits = relationship("RaceCircuit", back_populates="season")
    

class RaceCircuit(Base):
    __tablename__ = "race_circuits"
    
    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False, index=True)
    circuit = Column(String, nullable=True)
    date = Column(Date, nullable=True)  # Changed from String to Date type
    
    # Relationships
    season = relationship("Season", back_populates="race_circuits")
    results = relationship("ResultsRace", back_populates="race_circuit")
    

class ResultsRace(Base):
    __tablename__ = "results_race"
    
    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, ForeignKey("riders.id"), nullable=False, index=True)
    race_circuit_id = Column(Integer, ForeignKey("race_circuits.id"), nullable=False, index=True)
    position = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    
    # Relationships
    rider = relationship("Rider", back_populates="results")
    race_circuit = relationship("RaceCircuit", back_populates="results")
    