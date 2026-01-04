import sys
import os

# Add project root to PYTHONPATH
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)




# app/streamlit_app.py
import streamlit as st
import pandas as pd
import os
import joblib
from datetime import datetime
import plotly.express as px
# from src.etl import load_data, compute_kpis
# from src.features import make_features
# from src.staff_optimizer import optimize_staffz
from src.etl import load_data, compute_kpis
from src.features import make_features
from src.staff_optimizer import optimize_staff


st.set_page_config(page_title="Sort Center Workforce Analytics", layout="wide")

st.title("Sort Center — Workforce Planning & Performance Analytics")

@st.cache_data
def load():
    events, roster = load_data()
    kpi = compute_kpis(events)
    df_feat = make_features(kpi)
    return events, roster, kpi, df_feat

events, roster, kpi, df_feat = load()

# KPI summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total events", int(kpi['events_count'].sum()))
col2.metric("Avg UPH", round(kpi['UPH'].mean(),1))
col3.metric("Avg Processing sec", round(kpi['mean'].mean(),1))
col4.metric("Avg error rate", f"{(kpi['error_rate'].mean()*100):.2f}%")

# Time series UPH
st.subheader("UPH (Hourly)")
fig = px.line(kpi, x='hour', y='UPH', title='Units per Hour')
st.plotly_chart(fig, use_container_width=True)

# Shift comparison
st.subheader("Shift comparison")
# compute shift buckets using roster (simple mapping)
def assign_shift(hour):
    h = hour.hour
    if 6 <= h < 14:
        return 'A'
    if 14 <= h < 22:
        return 'B'
    return 'C'

kpi['shift'] = kpi['hour'].apply(assign_shift)
shift_summary = kpi.groupby('shift')['UPH'].agg(['mean','median','count']).reset_index()
st.dataframe(shift_summary)

# Leaderboard — top employees by count
st.subheader("Top employees by event count")
emp_counts = events.groupby('employee_id').size().reset_index(name='events')
st.table(emp_counts.sort_values('events', ascending=False).head(10))

# Prediction (if model exists)
st.subheader("UPH prediction (next hour)")
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'uph_model.joblib')
if os.path.exists(model_path):
    model = joblib.load(model_path)
    latest = df_feat.sort_values('hour').iloc[-1:]
    X = latest[['UPH','UPH_lag1','UPH_ma3','hour_of_day','dow','UPH_pct_change']]
    pred = model.predict(X)[0]
    st.write(f"Predicted UPH next hour: **{pred:.1f}**")
else:
    st.info("Model not found. Run `python src/train_model.py` to train a model.")

# Staffing optimizer
st.subheader("Staffing Recommendation")
per_worker_capacity = st.slider("Assumed UPH per worker", min_value=10, max_value=120, value=45)
opt_df = optimize_staff(kpi, per_worker_capacity=per_worker_capacity)
fig2 = px.bar(opt_df, x='hour', y='recommended_staff', title='Recommended staff per hour')
st.plotly_chart(fig2, use_container_width=True)
st.dataframe(opt_df.head(24))

# Anomaly detection (simple z-score)
st.subheader("Anomaly detection (UPH z-score)")
kpi['UPH_z'] = (kpi['UPH'] - kpi['UPH'].mean()) / kpi['UPH'].std()
anom = kpi[kpi['UPH_z'].abs() > 2]
st.write(f"Anomalous hours (|z|>2): {len(anom)}")
if len(anom) > 0:
    st.table(anom[['hour','UPH','UPH_z','error_rate']])

st.sidebar.header("Data & Controls")
st.sidebar.write("Events records:", len(events), "rows")
st.sidebar.download_button("Download hourly KPIs CSV", data=kpi.to_csv(index=False), file_name="hourly_kpis.csv")
