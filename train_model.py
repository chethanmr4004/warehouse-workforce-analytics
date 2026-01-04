# src/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
import os
from src.etl import load_data, compute_kpis
from src.features import make_features

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

def train_and_save():
    events, roster = load_data()
    kpi = compute_kpis(events)
    df = make_features(kpi)
    # target is next hour UPH
    df['target'] = df['UPH'].shift(-1)
    df = df.dropna()
    X = df[['UPH','UPH_lag1','UPH_ma3','hour_of_day','dow','UPH_pct_change']]
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print('R2 score:', score)
    joblib.dump(model, os.path.join(MODEL_DIR, 'uph_model.joblib'))
    print('Saved model to models/uph_model.joblib')

if __name__ == "__main__":
    train_and_save()
