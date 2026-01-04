# src/features.py
import pandas as pd

def make_features(kpi):
    df = kpi.copy().sort_values('hour')
    df['hour_of_day'] = df['hour'].dt.hour
    df['dow'] = df['hour'].dt.dayofweek
    # lag features
    df['UPH_lag1'] = df['UPH'].shift(1).fillna(method='bfill')
    df['UPH_ma3'] = df['UPH'].rolling(3, min_periods=1).mean()
    # percent change
    df['UPH_pct_change'] = df['UPH'].pct_change().fillna(0)
    return df
