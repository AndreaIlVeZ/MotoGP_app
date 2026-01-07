"""
ETL CLI entrypoint.
Usage: python -m app.etl input.pdf
"""

import sys
import argparse
import logging
from pathlib import Path

from app.backend.database import SessionLocal
from app.etl.pdf_tables import extract_tables_from_pdf, normalize_table
from app.etl.db_loader import load_results_to_db

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='MotoGP ETL Pipeline')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('--dry-run', action='store_true', help='Preview without loading')
    
    args = parser.parse_args()
    pdf_path = Path(args.pdf_path)
    
    if not pdf_path.exists():
        logger.error(f"File not found: {pdf_path}")
        sys.exit(1)
    
    try:
        # Extract
        logger.info(f"📄 Extracting from: {pdf_path}")
        tables = extract_tables_from_pdf(str(pdf_path))
        
        # Normalize
        import pandas as pd
        df = pd.concat([normalize_table(t) for t in tables], ignore_index=True)
        logger.info(f"✅ Found {len(df)} records")
        
        if args.dry_run:
            print(df.head(10))
            sys.exit(0)
        
        # Load
        logger.info("💾 Loading to database...")
        session = SessionLocal()
        try:
            stats = load_results_to_db(df, session)
            logger.info(f"✅ Done: {stats}")
        finally:
            session.close()
    
    except Exception as e:
        logger.error(f"❌ Failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()