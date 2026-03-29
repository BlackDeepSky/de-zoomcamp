# Data Engineering Capstone

**Belarus IT Job Market Analytics** — a batch pipeline that tracks Data Engineer, Data Analyst and Data Scientist vacancies on [rabota.by](https://rabota.by) (powered by HH.ru API). Monitors vacancy dynamics over time, required experience levels, and top-5 in-demand skills per role.

> **Course:** [Data Engineering Zoomcamp 2026](https://github.com/DataTalksClub/data-engineering-zoomcamp) by DataTalksClub
> **Constraint:** 100% local stack — no cloud services required.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        LOCAL STACK                              │
│                                                                 │
│  ┌──────────────┐    ┌──────────────────────────────────────┐   │
│  │  HH.ru API   │───▶│           Bruin Pipeline             │   │
│  │ (rabota.by)  │    │                                      │   │
│  └──────────────┘    │  ┌────────────────────────────────┐  │   │
│                      │  │  01_extract_hh.py  [BRONZE]    │  │   │
│                      │  │  Python · requests · pandas    │  │   │
│                      │  └───────────────┬────────────────┘  │   │
│                      │                  │ raw_vacancies      │   │
│                      │  ┌───────────────▼────────────────┐  │   │
│                      │  │  02_stg_vacancies.sql [SILVER] │  │   │
│                      │  │  Cleaning · date parsing       │  │   │
│                      │  └───────────┬──────────┬─────────┘  │   │
│                      │              │          │             │   │
│                      │  ┌───────────▼──┐  ┌───▼──────────┐  │   │
│                      │  │  03_mart_    │  │  04_mart_    │  │   │
│                      │  │  vacancies_  │  │  top_skills  │  │   │
│                      │  │  stats [GOLD]│  │  .sql [GOLD] │  │   │
│                      │  └───────────┬──┘  └───┬──────────┘  │   │
│                      └─────────────┼──────────┼─────────────┘   │
│                                    │          │                  │
│                      ┌─────────────▼──────────▼─────────────┐   │
│                      │         PostgreSQL (Docker)           │   │
│                      └──────────────────┬────────────────────┘   │
│                                         │                        │
│                      ┌──────────────────▼────────────────────┐   │
│                      │          Metabase (Docker)            │   │
│                      │     Dashboard · Charts · Filters      │   │
│                      └───────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Orchestration | [Bruin CLI](https://github.com/bruin-data/bruin) | Pipeline DAG, asset execution |
| Extraction | Python `requests` + `pandas` | HH.ru API parsing |
| Storage | PostgreSQL 15 (Docker) | Data warehouse |
| BI | Metabase (Docker) | Dashboard & visualization |
| Infrastructure | Docker Compose | Local environment |

---

## Pipeline Layers

### 🥉 Bronze — `01_extract_hh.py`
Hits the HH.ru API in two passes per vacancy: first a search query to get vacancy IDs, then a detail request per ID to extract `key_skills`. Collects up to 50 vacancies per role across 3 categories (Data Engineer, Data Analyst, Data Scientist) filtered to Belarus (`area=16`). Loads raw data into `public.raw_vacancies` via Bruin's `create+replace` strategy.

Fields collected: `id`, `role_category`, `title`, `published_at`, `experience`, `employer`, `skills`, `url`

### 🥈 Silver — `02_stg_vacancies.sql`
Cleans raw data and parses the ISO 8601 timestamp from the API into proper PostgreSQL types. Creates a view `public.stg_vacancies` with `published_date` (timestamptz) and `publish_day` (date) columns for downstream aggregation.

### 🥇 Gold — `03_mart_vacancies_stats.sql`
Aggregates vacancy counts grouped by `role_category`, `experience`, `publish_day`, `publish_week` and `publish_month`. Powers the vacancy dynamics chart in Metabase.

### 🥇 Gold — `04_mart_top_skills.sql`
Unpacks the comma-separated `skills` string using `STRING_TO_ARRAY` + `UNNEST`, counts mentions per skill per role, and ranks them with `ROW_NUMBER()`. Returns top-5 skills per profession.

---

## Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Bruin CLI](https://github.com/bruin-data/bruin) — `brew install bruin-data/tap/bruin`
- Python 3.11+

### 1. Clone & configure

```bash
git clone https://github.com/BlackDeepSky/de-zoomcamp.git
cd de-zoomcamp/Project
```

Create `.env` in the `Project/` directory:
```bash
POSTGRES_USER=data_engineer
POSTGRES_PASSWORD=strong_pass_123
POSTGRES_DB=movies_db
```

### 2. Start infrastructure

```bash
docker-compose up -d
docker-compose ps   # both containers should be healthy
```

### 3. Add Bruin connection

```bash
bruin connections add --env default --type postgres --name pg_local \
  --credentials '{"host":"localhost","port":5433,"username":"data_engineer","password":"strong_pass_123","database":"movies_db"}'

bruin connections list  # verify pg_local appears
```

### 4. Run the pipeline

```bash
# Validate all assets
bruin validate pipeline/

# Full run
bruin run pipeline/
```

Expected output:
```
PASS public.raw_vacancies
PASS public.stg_vacancies
PASS public.mart_vacancies_stats
PASS public.mart_top_skills

✓ Assets executed: 4 succeeded
```

### 5. Open Metabase dashboard

Navigate to **http://localhost:3000**

Connect to PostgreSQL using:
- Host: `postgres` (Docker service name)
- Port: `5432`
- Database: `movies_db`
- Username: `data_engineer`
- Password: `strong_pass_123`

---

## Project Structure

```
Project/
├── pipeline/
│   ├── assets/
│   │   ├── 01_extract_hh.py          # Bronze: API extraction
│   │   ├── 02_stg_vacancies.sql      # Silver: cleaning & typing
│   │   ├── 03_mart_vacancies_stats.sql  # Gold: vacancy dynamics
│   │   └── 04_mart_top_skills.sql    # Gold: top-5 skills
│   └── pipeline.yml                  # Bruin pipeline config
├── docker-compose.yaml               # PostgreSQL + Metabase
├── requirements.txt
└── .env                              # ← not committed
```

---

## Data Source

[HH.ru API](https://api.hh.ru) — public REST API, no authentication required for vacancy search. Rate limited to ~5 req/sec; pipeline uses `time.sleep(0.1)` between detail requests.

---

*Part of [Data Engineering Zoomcamp 2026](https://github.com/DataTalksClub/data-engineering-zoomcamp) capstone project.*
