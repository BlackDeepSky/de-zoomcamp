# Module 7 Homework: Stream Processing with Redpanda, PyFlink, and PostgreSQL

Real-time streaming pipeline built with Redpanda (Kafka-compatible broker), Apache Flink, and PostgreSQL for the Data Engineering Zoomcamp 2026. The pipeline ingests NYC Green Taxi trip data, processes it through Kafka producers/consumers and PyFlink jobs, and writes aggregated results to PostgreSQL.

## Pipeline Architecture

```
Producer (Python) -> Redpanda (Kafka) -> PyFlink Jobs -> PostgreSQL
```

## Tech Stack

| Tool | Version |
| --- | --- |
| Redpanda | v25.3.9 |
| Apache Flink | 2.2.0 |
| PyFlink | 2.2.0 |
| PostgreSQL | 18 |
| Python | 3.12 |
| uv | latest |

## Project Structure

```
hw7/
├── src/
│   ├── producers/
│   │   └── producer_hw7.py        # Sends green taxi data to Redpanda
│   ├── consumers/
│   │   └── consumer_hw7.py        # Reads from topic, counts trips > 5km
│   └── job/
│       ├── tumbling_job.py        # Q4: 5-min tumbling window by PULocationID
│       ├── session_job.py         # Q5: Session window with 5-min gap
│       └── tips_job.py            # Q6: 1-hour tumbling window for tip_amount
├── docker-compose.yml             # Redpanda, Flink JobManager/TaskManager, PostgreSQL
├── Dockerfile.flink               # Custom Flink image with Python 3.12 and PyFlink
├── flink-config.yaml              # Flink configuration
├── pyproject.flink.toml           # Dependencies for Flink container
├── pyproject.toml                 # Local Python dependencies
├── Makefile
├── uv.lock
└── README.md
```

## Quick Start

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Python dependencies

```bash
uv sync
```

### 3. Build and start all services

```bash
docker compose build
docker compose up -d
```

> ⚠️ If port 5432 is already in use (local PostgreSQL), change the postgres port in `docker-compose.yml`:
> `"5433:5432"` instead of `"5432:5432"`

Verify all 4 services are running:

```bash
docker compose ps
```

```
workshop-jobmanager-1    pyflink-workshop   Up   0.0.0.0:8081->8081/tcp
workshop-taskmanager-1   pyflink-workshop   Up
workshop-redpanda-1      redpandadata/...   Up   0.0.0.0:9092->9092/tcp
workshop-postgres-1      postgres:18        Up   0.0.0.0:5433->5432/tcp
```

Check Flink UI at http://localhost:8081

### 4. Create Kafka topic

```bash
docker exec -it workshop-redpanda-1 rpk topic create green-trips
```

### 5. Send data to Redpanda

```bash
uv run python src/producers/producer_hw7.py
```

### 6. Create PostgreSQL tables

```bash
docker exec -it workshop-postgres-1 psql -U postgres -d postgres -c "
CREATE TABLE green_trips_5min (
    window_start TIMESTAMP,
    PULocationID INTEGER,
    num_trips BIGINT,
    PRIMARY KEY (window_start, PULocationID)
);

CREATE TABLE green_trips_sessions (
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    PULocationID INTEGER,
    num_trips BIGINT,
    PRIMARY KEY (window_start, window_end, PULocationID)
);

CREATE TABLE green_trips_hourly_tips (
    window_start TIMESTAMP,
    total_tip DOUBLE PRECISION,
    PRIMARY KEY (window_start)
);"
```

### 7. Submit Flink jobs

```bash
# Q4 - Tumbling window
docker exec -it workshop-jobmanager-1 flink run \
    -py /opt/src/job/tumbling_job.py -d

# Q5 - Session window (cancel previous job first)
docker exec -it workshop-jobmanager-1 flink run \
    -py /opt/src/job/session_job.py -d

# Q6 - Hourly tips (cancel previous job first)
docker exec -it workshop-jobmanager-1 flink run \
    -py /opt/src/job/tips_job.py -d
```

> ⚠️ Cancel each job from Flink UI (http://localhost:8081) before starting the next one.
> Wait 2-3 minutes after submission before querying PostgreSQL.

---

## Questions, Queries & Answers

### Q1 — Redpanda Version

```bash
docker exec -it workshop-redpanda-1 rpk version
```

**Answer: `v25.3.9`**

---

### Q2 — Sending Data to Redpanda

Data: [green_tripdata_2025-10.parquet](https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet)

```bash
uv run python src/producers/producer_hw7.py
# Loaded 49,416 rows
# Sent 49,416 messages in 9.28 seconds
```

**Answer: `10 seconds`**

---

### Q3 — Consumer: Trips with distance > 5 km

```bash
uv run python src/consumers/consumer_hw7.py
```

```
Total messages: 49,416
Trips with trip_distance > 5: 8,506
```

**Answer: `8,506`**

---

### Q4 — Tumbling Window: Most Trips per PULocationID (5-min window)

```bash
docker exec -it workshop-jobmanager-1 flink run \
    -py /opt/src/job/tumbling_job.py -d
```

```sql
SELECT PULocationID, num_trips
FROM green_trips_5min
ORDER BY num_trips DESC
LIMIT 3;
```

```
 pulocationid | num_trips
--------------+-----------
           74 |        15
           74 |        14
           74 |        13
```

**Answer: `74`**

---

### Q5 — Session Window: Longest Streak (5-min gap)

```bash
docker exec -it workshop-jobmanager-1 flink run \
    -py /opt/src/job/session_job.py -d
```

```sql
SELECT PULocationID, num_trips
FROM green_trips_sessions
ORDER BY num_trips DESC
LIMIT 5;
```

```
 pulocationid | num_trips
--------------+-----------
           75 |        81
```

**Answer: `81`**

---

### Q6 — Tumbling Window: Hour with Highest Total Tip (1-hour window)

```bash
docker exec -it workshop-jobmanager-1 flink run \
    -py /opt/src/job/tips_job.py -d
```

```sql
SELECT window_start, total_tip
FROM green_trips_hourly_tips
ORDER BY total_tip DESC
LIMIT 3;
```

```
     window_start     | total_tip
---------------------+-----------
 2025-10-16 18:00:00 |    524.96
 2025-10-30 16:00:00 |    507.10
 2025-10-10 17:00:00 |    499.60
```

**Answer: `2025-10-16 18:00:00`**

---

## Results Summary

| # | Question | Answer |
|---|----------|--------|
| Q1 | Redpanda version | `v25.3.9` |
| Q2 | Time to send data | `10 seconds` |
| Q3 | Trips with distance > 5 km | `8,506` |
| Q4 | PULocationID with most trips (5-min window) | `74` |
| Q5 | Longest session streak (trips) | `81` |
| Q6 | Hour with highest total tip | `2025-10-16 18:00:00` |

## Data Source

NYC Taxi and Limousine Commission (TLC) Trip Record Data:

```
https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet
```

---

Built as part of **[Data Engineering Zoomcamp 2026](https://github.com/DataTalksClub/data-engineering-zoomcamp)** by DataTalksClub — a free, open-source data engineering course covering the full modern data stack.
