"""
Analytics Module - Portfolio calculations
Includes ROI, Risk, and Growth calculations
"""
import pandas as pd
import numpy as np

def calculate_roi(df):
    """
    Calculate Return on Investment (ROI) for portfolio
    
    ROI % = ((Current Value - Investment Amount) / Investment Amount) * 100
    """
    if df.empty:
        return df
    
    try:
        # Ensure required columns exist
        if 'investment_amount' in df.columns and 'current_value' in df.columns:
            df['roi_amount'] = df['current_value'] - df['investment_amount']
            df['roi_percent'] = ((df['current_value'] - df['investment_amount']) / df['investment_amount']) * 100
            
            # Round for better display
            df['roi_percent'] = df['roi_percent'].round(2)
            df['roi_amount'] = df['roi_amount'].round(2)
        else:
            # If columns missing, add with default values
            df['roi_percent'] = 0
            df['roi_amount'] = 0
            
    except Exception as e:
        print(f"Error calculating ROI: {e}")
        df['roi_percent'] = 0
        df['roi_amount'] = 0
    
    return df

def calculate_risk(df):
    """
    Calculate risk level and risk score for each investment
    
    Risk is based on:
    - Asset type volatility
    - ROI variance
    - Investment amount
    """
    if df.empty:
        return df
    
    try:
        # Define risk scores for asset types (can be customized)
        asset_risk_scores = {
            'stocks': 7,
            'equity': 7,
            'crypto': 9,
            'cryptocurrency': 9,
            'real estate': 4,
            'realestate': 4,
            'bonds': 3,
            'fixed deposit': 2,
            'fd': 2,
            'savings': 1,
            'mutual funds': 5,
            'mutualfunds': 5,
            'gold': 4,
            'commodities': 6
        }
        
        # Calculate base risk score from asset type
        if 'asset_type' in df.columns:
            df['risk_score'] = df['asset_type'].str.lower().map(asset_risk_scores).fillna(5)
        else:
            df['risk_score'] = 5
        
        # Adjust risk based on ROI volatility if multiple investments
        if 'roi_percent' in df.columns and len(df) > 1:
            roi_std = df.groupby('asset_type')['roi_percent'].transform('std').fillna(0)
            df['risk_score'] = df['risk_score'] + (roi_std / 10).clip(0, 3)
        
        # Ensure risk_score is between 1-10
        df['risk_score'] = df['risk_score'].clip(1, 10).round(1)
        
        # Categorize into risk levels
        df['risk_level'] = pd.cut(
            df['risk_score'],
            bins=[0, 3.5, 6.5, 10],
            labels=['Low', 'Medium', 'High']
        )
        
    except Exception as e:
        print(f"Error calculating risk: {e}")
        df['risk_score'] = 5
        df['risk_level'] = 'Medium'
    
    return df

def calculate_growth(df):
    """
    Calculate portfolio growth metrics
    
    Includes:
    - CAGR (Compound Annual Growth Rate)
    - Time-weighted returns
    - Ending value projections
    """
    if df.empty:
        return df
    
    try:
        # Calculate time period if dates available
        if 'investment_start_date' in df.columns:
            df['investment_start_date'] = pd.to_datetime(df['investment_start_date'], errors='coerce')
            current_date = pd.Timestamp.now()
            df['days_invested'] = (current_date - df['investment_start_date']).dt.days
            df['years_invested'] = (df['days_invested'] / 365.25).clip(lower=0.01)  # Avoid division by zero
        else:
            # Default to 1 year if no date
            df['years_invested'] = 1
            df['days_invested'] = 365
        
        # Calculate CAGR (Compound Annual Growth Rate)
        if 'investment_amount' in df.columns and 'current_value' in df.columns:
            df['cagr_percent'] = (
                ((df['current_value'] / df['investment_amount']) ** (1 / df['years_invested']) - 1) * 100
            ).round(2)
            
            # Calculate ending value (same as current value for now)
            df['ending_value'] = df['current_value']
        else:
            df['cagr_percent'] = 0
            df['ending_value'] = df.get('investment_amount', 0)
        
        # Handle infinite/NaN values
        df['cagr_percent'] = df['cagr_percent'].replace([np.inf, -np.inf], 0).fillna(0)
        
    except Exception as e:
        print(f"Error calculating growth: {e}")
        df['cagr_percent'] = 0
        df['ending_value'] = df.get('current_value', df.get('investment_amount', 0))
        df['years_invested'] = 1
    
    return df

def get_portfolio_summary(df, client_id=None):
    """
    Get summary statistics for a portfolio
    """
    if client_id:
        df = df[df['client_id'] == client_id]
    
    if df.empty:
        return {}
    
    summary = {
        'total_invested': df['investment_amount'].sum() if 'investment_amount' in df.columns else 0,
        'total_current_value': df['current_value'].sum() if 'current_value' in df.columns else 0,
        'total_profit_loss': (df['current_value'].sum() - df['investment_amount'].sum()) 
                            if 'investment_amount' in df.columns and 'current_value' in df.columns else 0,
        'avg_roi': df['roi_percent'].mean() if 'roi_percent' in df.columns else 0,
        'total_assets': len(df),
        'asset_types': df['asset_type'].nunique() if 'asset_type' in df.columns else 0
    }
    
    return summary