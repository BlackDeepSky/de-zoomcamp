# Homework 6: Batch Processing with Apache Spark
**Data Engineering Zoomcamp 2026**

## Stack
- Python 3.13
- PySpark 3.5.3
- Java 17 (Temurin)
- Jupyter Notebook

---

## Setup

### 1. Java 17
Скачай и установи JDK 17: https://adoptium.net/temurin/releases/?version=17&os=mac&arch=x64&package=jdk

> ⚠️ Java 25 и PySpark 3.5.3 несовместимы. Используй строго **Java 17**.

Проверь:
```bash
java -version
# openjdk version "17..."
```

### 2. Создай и активируй виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установи зависимости
```bash
pip install pyspark==3.5.3 jupyter ipykernel
```

> ⚠️ PySpark 4.x несовместим с Java 17/21/25. Используй строго **3.5.3**.

### 4. Зарегистрируй venv как Jupyter kernel
```bash
python -m ipykernel install --user --name=venv --display-name "Python (venv)"
```

### 5. Запускай Jupyter с явным указанием JAVA_HOME
```bash
cd ~/Desktop/de-zoomcamp/hw6
source venv/bin/activate
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
jupyter notebook notebooks/homework6.ipynb
```

В Jupyter выбери kernel: **Kernel → Change Kernel → Python (venv)**

Данные (~68 MB) скачаются автоматически при первом запуске.

---

## Структура проекта
```
hw6/
├── notebooks/
│   └── homework6.ipynb   # основное решение
├── data/                 # скачивается автоматически (в .gitignore)
├── venv/                 # виртуальное окружение (в .gitignore)
└── README.md
```

---

## Ответы

| # | Вопрос | Ответ |
|---|--------|-------|
| Q1 | Версия Spark | `3.5.3` |
| Q2 | Размер файла yellow_tripdata_2025-11.parquet | `67.8 MB` (~75MB) |
| Q3 | Кол-во поездок 15 ноября 2025 | `162,604` |
| Q4 | Длительность самой долгой поездки | `90.6 часов` |
| Q5 | Порт Spark UI | `4040` |
| Q6 | Зона с наименьшим числом посадок | `Governor's Island/Ellis Island/Liberty Island` |

---

## Данные
- Yellow Taxi November 2025: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet
- Taxi Zone Lookup: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv