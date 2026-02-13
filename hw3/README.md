# 🗄️ Data Engineering Zoomcamp — Lesson 3: Data Warehouse

> **Course**: [Data Engineering Zoomcamp 2026](https://github.com/DataTalksClub/data-engineering-zoomcamp)  
> **Lesson**: 03 — Data Warehouse (BigQuery concepts)  
> **Execution**: ✅ Completed locally via DuckDB (no cloud access)

---
```bash
pip install -r requirements.txt
```
```bash
# 1. Download NYC Taxi data for 2024 (Jan-Jun)
python download_data.py

# 2. Execute homework assignment
python homework.py

# 3. (Optional) Deactivate virtual environment when finished
deactivate
```
---
## 🌍 Execution Context

Due to geographic restrictions limiting access to cloud platforms (AWS/GCP/Azure) from Belarus, this assignment was executed **locally using DuckDB** with full preservation of conceptual learning objectives:

| Aspect | Official Course Approach | Local Implementation |
|--------|--------------------------|----------------------|
| **Platform** | Google BigQuery (GCP) | DuckDB (local execution) |
| **Storage** | Google Cloud Storage bucket | Local Parquet files (`./data/`) |
| **Byte measurements** | Exact values from BigQuery UI (e.g., 155.12 MB) | Conceptual demonstration via query behavior |
| **Learning objective** | Understand partitioning/clustering/columnar storage | ✅ Fully achieved |

> 💡 **Key principle**: Data engineering concepts (partitioning, clustering, columnar storage) are **universal** — they apply identically across BigQuery, Snowflake, Redshift, and are demonstrable via DuckDB's Parquet integration.

---

## Core Concepts Demonstrated
1. **Partitioning**
Concept: Physical data separation by partition key (typically datetime)
Local demonstration: Created trips_optimized table ordered by DATE(tpep_pickup_datetime)
Benefit observed: Date-range queries leverage data locality (faster execution on ordered data)
Cloud equivalent: PARTITION BY DATE(tpep_pickup_datetime) in BigQuery

2. **Clustering**
Concept: Intra-partition data ordering by frequently filtered columns
Local demonstration: Combined ordering by DATE(tpep_pickup_datetime), VendorID
Benefit observed: Optimized ORDER BY and GROUP BY operations on clustered columns
Cloud equivalent: CLUSTER BY VendorID in BigQuery