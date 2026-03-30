{{ config(
    materialized='table',
    post_hook="CREATE INDEX IF NOT EXISTS idx_mart_stats_day ON {{ this }} (publish_day)"
) }}

SELECT
    role_category,
    experience,
    publish_day,
    DATE_TRUNC('week', publish_day)  AS publish_week,
    DATE_TRUNC('month', publish_day) AS publish_month,
    COUNT(DISTINCT id)               AS vacancies_count
FROM {{ source('public', 'stg_vacancies') }}
GROUP BY 1, 2, 3, 4, 5
