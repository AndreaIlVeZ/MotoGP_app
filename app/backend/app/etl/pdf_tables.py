import pandas as pd
import numpy as np

from typing import List


#### file has to change radically, has to import the pdfs from supabase

## store them in dataframes that need to be quickly validated
## pushed to databases

## class extraction from supabase
    
## class to clean and transform
    ## extract the data properly
    ## store them in dataframes that need to be quickly validated on the go (in memory)
## pushed to databases
## testing part

## class to push to postgres

def extract_tables_from_pdf(path: str) -> List[pd.DataFrame]:

    #### placeholder function data is not thewre yer
    return clean_table



def normalize_table(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    # Handle missing values
    df.replace({"": np.nan, "N/A": np.nan}, inplace=True)
    
    # Convert data types
    for col in df.select_dtypes(include=["object"]).columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except ValueError:
            pass  # If conversion fails, keep as object
    
    return df