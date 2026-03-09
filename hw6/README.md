# Module 6 Homework: Batch Processing with Apache Spark

Batch data processing with PySpark for the Data Engineering Zoomcamp 2026. The notebook loads NYC Yellow Taxi trip data for November 2025, runs analytical queries using Spark DataFrames, and answers all six homework questions.

## Project Structure

```
hw6/
├── notebooks/
│   └── homework6.ipynb   # Main solution notebook
├── data/                 # Downloaded automatically (gitignored)
├── venv/                 # Virtual environment (gitignored)
└── README.md
```

## Tech Stack

| Tool | Version |
| --- | --- |
| Python | 3.13 |
| PySpark | 3.5.3 |
| Java | 17 (Temurin) |
| Jupyter Notebook | latest |

## Quick Start

### 1. Install Java 17

Download and install JDK 17: https://adoptium.net/temurin/releases/?version=17&os=mac&arch=x64&package=jdk

> ⚠️ Java 25 is incompatible with PySpark 3.5.3 due to Hadoop's `getSubject` issue. Use strictly **Java 17**.

Verify:
```bash
java -version
# openjdk version "17..."
```

### 2. Create and activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install pyspark==3.5.3 jupyter ipykernel
```

> ⚠️ PySpark 4.x is incompatible with Java 17/21/25. Use strictly **3.5.3**.

### 4. Register venv as Jupyter kernel

```bash
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```

### 5. Launch Jupyter with explicit JAVA_HOME

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
jupyter notebook notebooks/homework6.ipynb
```

Select kernel: **Kernel → Change Kernel → Python (venv)**

Data files (~68 MB) are downloaded automatically on first run.

## What the Notebook Does

| Step | Description |
| --- | --- |
| SparkSession init | Creates a local Spark session with `local[*]` |
| Data download | Fetches Parquet + zone lookup CSV from NYC TLC |
| Q2 | Measures raw file size on disk |
| Q3 | Filters trips by pickup date, counts records |
| Q4 | Computes trip duration in hours, finds maximum |
| Q5 | Reads Spark UI URL from SparkContext |
| Q6 | Groups by pickup zone, joins with zone lookup, sorts ascending |

## Results

| Question | Answer |
| --- | --- |
| Q1 — Spark version | `3.5.3` |
| Q2 — File size | `67.8 MB` (~75 MB) |
| Q3 — Trips on November 15, 2025 | `162,604` |
| Q4 — Longest trip duration | `90.6 hours` |
| Q5 — Spark UI port | `4040` |
| Q6 — Least frequent pickup zone | `Governor's Island/Ellis Island/Liberty Island` |

## Data Sources

NYC Taxi and Limousine Commission (TLC) Trip Record Data — publicly available Parquet files:

```
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet
https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

---

Built as part of **[Data Engineering Zoomcamp 2026](https://github.com/DataTalksClub/data-engineering-zoomcamp)** by DataTalksClub — a free, open-source data engineering course covering the full modern data stack.