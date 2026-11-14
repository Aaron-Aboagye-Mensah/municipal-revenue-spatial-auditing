import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
# 1. SIMULATE MUNICIPAL REVENUE & SPATIAL CENSUS RECORDS
np.random.seed(42)
n_records = 500
data = pd.DataFrame({
"Zone_ID": np.random.choice(["Zone_A_North", "Zone_B_Central", "Zone_C_South",
"Zone_D_West"], n_records),
"Property_Type": np.random.choice(["Commercial", "Residential", "Industrial"],
n_records, p=[0.35, 0.50, 0.15]),
"GPS_Latitude": np.round(np.random.uniform(5.55, 5.65, n_records), 5),
"GPS_Longitude": np.round(np.random.uniform(-0.28, -0.18, n_records), 5),
"Expected_Rate_GHS": np.random.normal(loc=1200, scale=300,
size=n_records).round(2),
"Collected_Amount_GHS": np.random.normal(loc=1180, scale=310,
size=n_records).round(2),
"Days_Late": np.random.randint(0, 45, n_records)
})
# Inject realistic anomalies (revenue leakage, under-collection, & GPS boundary
outliers)
data.loc[10:18, "Collected_Amount_GHS"] = data.loc[10:18, "Expected_Rate_GHS"] *
0.12 # Severe under-collection
data.loc[25:28, "GPS_Latitude"] = 6.85000 # Spatial coordinate outlier outside
district
# 2. DATA CLEANING & FEATURE ENGINEERING
data["Expected_Rate_GHS"] = data["Expected_Rate_GHS"].clip(lower=100)
data["Collected_Amount_GHS"] = data["Collected_Amount_GHS"].clip(lower=0)
data["Collection_Ratio"] = (data["Collected_Amount_GHS"] /
data["Expected_Rate_GHS"]).round(3)
data["Revenue_Variance_GHS"] = (data["Collected_Amount_GHS"] -
data["Expected_Rate_GHS"]).round(2)
# 3. SPATIAL VALIDATION CHECK (DISTRICT BOUNDING BOX)
valid_lat = data["GPS_Latitude"].between(5.50, 5.70)
valid_lon = data["GPS_Longitude"].between(-0.35, -0.10)
data["Spatial_Valid"] = valid_lat & valid_lon
# 4. MACHINE LEARNING ANOMALY DETECTION (ISOLATION FOREST)
features = ["Expected_Rate_GHS", "Collected_Amount_GHS", "Collection_Ratio",
"Days_Late"]
model = IsolationForest(contamination=0.05, random_state=42)
data["Anomaly_Flag"] = model.fit_predict(data[features])
data["Audit_Status"] = np.where((data["Anomaly_Flag"] == -1) |
(~data["Spatial_Valid"]), "FLAGGED_FOR_AUDIT", "VERIFIED")
# 5. SUMMARY REPORT BY ZONE
summary = data.groupby("Zone_ID").agg(
Total_Accounts=("Zone_ID", "count"),
Expected_Total=("Expected_Rate_GHS", "sum"),
Collected_Total=("Collected_Amount_GHS", "sum"),
Flagged_Cases=("Audit_Status", lambda x: (x == "FLAGGED_FOR_AUDIT").sum())
).reset_index()
summary["Collection_Efficiency_%"] = ((summary["Collected_Total"] /
summary["Expected_Total"]) * 100).round(2)
print("=== MUNICIPAL REVENUE & SPATIAL
