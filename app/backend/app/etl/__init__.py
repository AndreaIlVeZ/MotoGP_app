"""
ETL package for loading MotoGP data from PDFs to PostgreSQL.
"""

from .pdf_tables import extract_tables_from_pdf, normalize_table
from .db_loader import load_results_to_db

__all__ = [
    'extract_tables_from_pdf',
    'normalize_table', 
    'load_results_to_db',
]