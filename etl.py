# src/etl.py
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_data(events_path=None, roster_path=None):
    events_path = events_path or os.path.join(DATA_DIR, 'sample_events.csv')
    roster_path = roster_path or os.path.join(DATA_DIR, 'sample_roster.csv')
    events = pd.read_csv(events_path, parse_dates=['timestamp'])
    roster = pd.read_csv(roster_path, parse_dates=['shift_start','shift_end'])
    return events, roster

def compute_kpis(events):
    # create hour bucket
    events['hour'] = events['timestamp'].dt.floor('H')
    # units per hour (count of package events that are dispatch/scan/sort depending on KPI)
    uph = events.groupby('hour').size().rename('events_count').reset_index()
    # processing time summary per hour
    proc = events.groupby('hour')['processing_seconds'].agg(['mean','median','sum']).reset_index().rename(columns={'sum':'proc_sum'})
    errors = events.groupby('hour')['error_flag'].sum().reset_index().rename(columns={'error_flag':'errors'})
    # merge
    kpi = uph.merge(proc, on='hour').merge(errors, on='hour')
    # compute UPH approximate (assuming events roughly map to units)
    kpi['UPH'] = (kpi['events_count'] / 1.0).round(1)
    kpi['error_rate'] = (kpi['errors'] / kpi['events_count']).fillna(0)
    return kpi

if __name__ == "__main__":
    events, roster = load_data()
    kpi = compute_kpis(events)
    print(kpi.head())
    kpi.to_csv(os.path.join(DATA_DIR, 'hourly_kpis.csv'), index=False)
    print('Saved hourly_kpis.csv')