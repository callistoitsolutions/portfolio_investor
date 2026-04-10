"""
Data Loader Module - File-based storage
Loads and saves portfolio data from/to CSV files
"""
import pandas as pd
from pathlib import Path
import os

# Data file path
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_FILE = DATA_DIR / "portfolio_data.csv"

def load_portfolio_data():
    """
    Load portfolio data from CSV file
    Returns empty DataFrame if file doesn't exist
    """
    try:
        if DATA_FILE.exists():
            df = pd.read_csv(DATA_FILE)
            
            # Convert date columns if they exist
            date_columns = ['investment_start_date', 'investment_end_date', 'date']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            return df
        else:
            # Return empty DataFrame with expected structure
            return pd.DataFrame(columns=[
                'client_id', 'asset_type', 'investment_amount', 
                'current_value', 'investment_start_date'
            ])
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def save_portfolio_data(df):
    """
    Save portfolio data to CSV file
    """
    try:
        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        df.to_csv(DATA_FILE, index=False)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def get_data_path():
    """Return the data file path"""
    return str(DATA_FILE)