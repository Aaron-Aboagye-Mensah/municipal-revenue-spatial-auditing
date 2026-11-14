Municipal Revenue & Spatial Census Data Auditing Pipeline
## Overview
An end-to-end Python data auditing and anomaly detection pipeline modeled on realworld
municipal revenue mobilization and digital E-Census spatial validation
workflows.
## Key Capabilities
- **Data Cleaning & Variance Engineering:** Calculates collection ratios and net
revenue leakage across commercial, residential, and industrial zones.
- **Geospatial Coordinate Validation:** Flags GPS boundary discrepancies to ensure
enumeration completeness.
- **Unsupervised Anomaly Detection:** Uses `scikit-learn` Isolation Forest to
isolate high-risk accounts for compliance review.
## Tech Stack
Python 3 | pandas | NumPy | scikit-learn
