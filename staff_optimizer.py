# src/staff_optimizer.py
import pandas as pd
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpInteger, value
import os
from src.etl import load_data, compute_kpis
from src.features import make_features

def optimize_staff(kpi_df, per_worker_capacity=40):
    """
    per_worker_capacity: expected units per hour by an average worker (UPH per worker)
    Returns: DataFrame with recommended headcount per hour
    """
    df = kpi_df.copy().sort_values('hour')
    # set target as observed UPH (or higher)
    df['target_uph'] = df['UPH'].values
    hours = range(len(df))
    prob = LpProblem('staffing', LpMinimize)
    x = [LpVariable(f'x_{i}', lowBound=0, cat=LpInteger) for i in hours]
    # objective minimize total staff-hours
    prob += lpSum(x)
    # constraints: capacity must meet target
    for i in hours:
        prob += x[i] * per_worker_capacity >= df.iloc[i]['target_uph']
    prob.solve()
    df['recommended_staff'] = [int(v.value()) for v in x]
    df['per_worker_capacity'] = per_worker_capacity
    return df[['hour','UPH','target_uph','recommended_staff','per_worker_capacity']]

if __name__ == "__main__":
    events, roster = load_data()
    kpi = compute_kpis(events)
    out = optimize_staff(kpi, per_worker_capacity=45)
    print(out.head())
