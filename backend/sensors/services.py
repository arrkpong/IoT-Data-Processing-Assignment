# backend\sensors\services.py
import pandas as pd
import numpy as np
from scipy import stats

def clean_and_flag(df: pd.DataFrame) -> pd.DataFrame:
    # 1. Drop exact duplicates
    df = df.drop_duplicates(subset=['timestamp'])
    # 2. Fill or interpolate missing values
    df = df.set_index('timestamp').sort_index()
    df = df.interpolate(method='time').reset_index()

    # 3. Flag anomalies via Z-score
    for col in ['temperature', 'humidity', 'air_quality']:
        z = np.abs(stats.zscore(df[col].ffill()))
        df[f'{col}_anomaly'] = (z > 3).astype(int)
    return df

def aggregate_stats(df: pd.DataFrame, window: str) -> dict:
    # e.g. window = '1H', '10min'
    df = df.set_index('timestamp').sort_index()
    window = window.lower()
    agg = df.resample(window).agg(['mean', 'median', 'min', 'max'])

    aggregated_data = {}
    for col in ['temperature', 'humidity', 'air_quality']:
        for stat in ['mean', 'median', 'min', 'max']:
            key = f"{col}_{stat}"
            values = agg[col][stat].tolist()
            # Filter out NaN values before adding to the dictionary
            aggregated_data[key] = [v for v in values if not pd.isna(v)]
    return aggregated_data