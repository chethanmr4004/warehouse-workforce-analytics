# src/simulate.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)

def generate_roster(num_employees=20, start_date='2025-11-01'):
    emp = []
    names = [f'Emp{str(i).zfill(3)}' for i in range(1, num_employees+1)]
    shifts = [('A','06:00','14:00'), ('B','14:00','22:00'), ('C','22:00','06:00')]
    for i, name in enumerate(names):
        shift = shifts[i % 3]
        emp_id = f'E{str(i+1).zfill(3)}'
        shift_start = datetime.fromisoformat(start_date + ' ' + shift[1])
        # adjust C shift end next day
        shift_end = shift_start + timedelta(hours=8)
        skill = round(np.clip(np.random.normal(0.8, 0.08), 0.5, 1.0), 2)
        emp.append({
            'employee_id': emp_id,
            'employee_name': name,
            'shift': shift[0],
            'shift_start': shift_start.strftime('%Y-%m-%d %H:%M'),
            'shift_end': shift_end.strftime('%Y-%m-%d %H:%M'),
            'skill_level': skill
        })
    df = pd.DataFrame(emp)
    df.to_csv(os.path.join(DATA_DIR, 'sample_roster.csv'), index=False)
    print('Wrote sample_roster.csv')
    return df

def generate_events(num_records=5000, start_date='2025-11-01'):
    base = datetime.fromisoformat(start_date + ' 06:00:00')
    stages = ['inbound','scan','sort','dispatch']
    scanners = [f'S{str(i).zfill(2)}' for i in range(1,11)]
    employees = [f'E{str(i).zfill(3)}' for i in range(1,21)]
    rows = []
    for i in range(1, num_records+1):
        t = base + timedelta(seconds=int(np.random.exponential(scale=30)*i % (3600*16)))
        pkg = f'P{str(10000+i)}'
        stage = np.random.choice(stages, p=[0.2,0.5,0.25,0.05])
        scanner = np.random.choice(scanners)
        emp = np.random.choice(employees)
        proc = int(np.clip(np.random.normal(10,4), 3, 60))
        # small chance of error
        error = int(np.random.rand() < 0.02)
        rows.append({
            'event_id': i,
            'package_id': pkg,
            'timestamp': t.strftime('%Y-%m-%d %H:%M:%S'),
            'stage': stage,
            'scanner_id': scanner,
            'employee_id': emp,
            'processing_seconds': proc,
            'error_flag': error
        })
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA_DIR, 'sample_events.csv'), index=False)
    print('Wrote sample_events.csv')
    return df

if __name__ == "__main__":
    generate_roster(20)
    generate_events(10000)
