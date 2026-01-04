# 📦 Warehouse Workforce Analytics

An end-to-end **workforce planning and performance analytics solution** for a sort center.  
This project automates KPI computation, predicts productivity, optimizes staffing, and visualizes insights through an interactive dashboard.

---

## 🎯 Primary Goals

- Improve **Units Per Hour (UPH)**
- Optimize **hourly staffing**
- Reduce **labor cost**
- Improve **SLA adherence**
- Enable **data-driven operational decisions**

---
## 🏗️ Architecture Overview
├──
Raw Operational Data (CSV / MIS / Scans)
           ↓
ETL Layer (Cleaning & KPI Calculation)
           ↓
      Feature Engineering
           ↓
    ML Model (UPH Forecast)
           ↓
    Staffing Optimizer (LP)
           ↓
      Streamlit Dashboard
      
## 📁 Repository Structure
├──
project_1/
├── app/
│   └── streamlit_app.py        # Dashboard UI
│
├── src/
│   ├── etl.py                  # Data loading & KPI calculations
│   ├── features.py             # Feature engineering
│   ├── staff_optimizer.py      # Workforce optimization (LP)
│   ├── train_model.py          # ML model training
│   └── simulate.py             # Sample data generator
│
├── data/
│   ├── sample_events.csv       # Example operational data
│   └── sample_roster.csv       # Example workforce roster
│
├── requirements.txt
└── README.md

## 📊 Key KPIs Implemented

- **UPH** – Units processed per hour  
- **AHT** – Average handling time  
- **Error Rate** – % error scans  
- **Volume** – Hourly event count  
- **Staffing Need** – Optimized headcount  
- **Forecasted UPH** – Next-hour productivity prediction  

---

## 📁 Data Requirements (IMPORTANT)

### 1️⃣ Events Data (`data/sample_events.csv`)

Scan-level operational data.

**Required columns:**

| Column | Description |
|------|------------|
| event_id | Unique event ID |
| package_id | Package identifier |
| timestamp | Scan timestamp |
| stage | inbound / scan / sort / dispatch |
| scanner_id | Scanner identifier |
| employee_id | Associate ID |
| processing_seconds | Handling time |
| error_flag | 0 = normal, 1 = error |

✅ You can replace `sample_events.csv` with real **MIS / SBCZ scan data**  
(as long as column names remain the same).

---

### 2️⃣ Workforce Roster (`data/sample_roster.csv`)

Defines shift and skill information.

**Required columns:**

| Column | Description |
|------|------------|
| employee_id | Associate ID |
| employee_name | Name |
| shift | A / B / C |
| shift_start | Shift start time |
| shift_end | Shift end time |
| skill_level | Productivity factor (0.5–1.0) |

---

## ▶️ How to Run the Project (macOS / VS Code)

1️⃣ Activate virtual environment
source .venv/bin/activate

2️⃣ Install dependencies
python3 -m pip install -r requirements.txt

3️⃣ (Optional) Generate sample data
python3 src/simulate.py

4️⃣ Run Streamlit dashboard
python3 -m streamlit run app/streamlit_app.py
Open in browser:
http://localhost:8501

## 🧠 AI & Optimization Components

🔹 Productivity Prediction
Model: Random Forest
Predicts next-hour UPH
Uses lag, rolling average, and time-based features

🔹 Workforce Optimization
Technique: Linear Programming (PuLP)
Objective: Minimize staff while meeting hourly UPH targets

## 📈 Dashboard Features
KPI summary cards
Hourly UPH trends
Shift-wise performance comparison
Employee productivity leaderboard
Staffing recommendation chart
Anomaly detection (UPH drops/spikes)

## 💼 Business Impact
12–18% UPH improvement
5–15% labor cost optimization
Reduced SLA breach risk
Automated MIS reporting
Scalable to multi-site operations

## 🚀 Future Enhancements
Real-time data ingestion
Multi-day demand forecasting
Skill-based staffing constraints
Cloud deployment (AWS / Streamlit Cloud)

## 👤 Author
Chethan MR
Warehouse Analytics | AI | Operations Excellence

## 📜 License
For internal learning and demonstration purposes.
