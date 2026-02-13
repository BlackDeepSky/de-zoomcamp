# DE Zoomcamp — Homework 1 (Docker, PostgreSQL, SQL)

## Описание
В данном задании было развернуто локальное окружение с использованием **Docker**, **PostgreSQL** и **pgAdmin**, загружены данные поездок такси и выполнены SQL-запросы для ответа на вопросы домашнего задания.

Все шаги были выполнены локально и результат опубликован в GitHub-репозитории.

---

## Используемые инструменты
- Docker & Docker Compose
- PostgreSQL
- pgAdmin
- SQL
- GitHub

---

## Окружение

Запуск сервисов:
```bash
docker compose up -d
```

Остановка сервисов:
```bash
docker compose down
```

Подключение к базе данных из pgAdmin:
- **Host**: `db`
- **Port**: `5432`
- **Database**: `postgres`
- **User**: `postgres`
- **Password**: `postgres`

---

## Ответы на вопросы и SQL-запросы

### Question 1  
**What's the version of pip in the python:3.13 image?**

**Ответ:** `25.3`

---

### Question 2  
**Hostname и port для подключения pgAdmin к PostgreSQL**

**Ответ:** `db:5432`

---

### Question 3  
**For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile?**

```sql
SELECT
    COUNT(*) AS trips_count
FROM green_taxi_trips
WHERE
    DATE(lpep_pickup_datetime) BETWEEN '2025-11-01' AND '2025-11-30'
    AND trip_distance <= 1;
```

**Ответ:** `8009`

---

### Question 4  
**Which was the pick up day with the longest trip distance (trip_distance < 100)?**

```sql
SELECT
    DATE(lpep_pickup_datetime) AS pickup_date,
    MAX(trip_distance) AS max_distance
FROM green_taxi_trips
WHERE
    trip_distance < 100
GROUP BY pickup_date
ORDER BY max_distance DESC
LIMIT 1;
```

**Ответ:** `2025-11-25`

---

### Question 5  
**Pickup zone with the largest total_amount on November 18th, 2025**

```sql
SELECT
    zpu.zone AS pickup_zone,
    SUM(t.total_amount) AS total_amount_sum
FROM green_taxi_trips t
JOIN zones zpu
    ON t.pulocationid = zpu.locationid
WHERE
    DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY pickup_zone
ORDER BY total_amount_sum DESC
LIMIT 1;
```

**Ответ:** `East Harlem North`

---

### Question 6  
**Drop-off zone with the largest tip for passengers picked up in "East Harlem North" (November 2025)**

```sql
SELECT
    zdo.zone AS dropoff_zone,
    SUM(t.tip_amount) AS total_tip
FROM green_taxi_trips t
JOIN zones zpu
    ON t.pulocationid = zpu.locationid
JOIN zones zdo
    ON t.dolocationid = zdo.locationid
WHERE
    zpu.zone = 'East Harlem North'
    AND DATE(t.lpep_pickup_datetime) BETWEEN '2025-11-01' AND '2025-11-30'
GROUP BY dropoff_zone
ORDER BY total_tip DESC
LIMIT 1;
```

**Ответ:** `JFK Airport`

---

### Question 7  
**Correct Terraform workflow**

**Ответ:**
```text
terraform init
terraform apply -auto-approve
terraform destroy
```

---

## Итог
В ходе выполнения задания:
- было развернуто воспроизводимое окружение в Docker;
- выполнено подключение к PostgreSQL через pgAdmin;
- написаны SQL-запросы с фильтрацией, агрегациями и JOIN;
- результаты задокументированы и опубликованы в GitHub.

---

## Репозиторий
https://github.com/BlackDeepSky/de-zoomcamp-hw1
