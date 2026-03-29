/*@bruin
name: public.mart_vacancies_stats
type: pg.sql
connection: pg_local
materialization:
  type: table
  strategy: create+replace
depends_on:
  - public.stg_vacancies
columns:
  - name: publish_day
    description: "Partition key — date of vacancy publication"
@bruin*/

SELECT
    role_category,
    experience,
    publish_day,
    DATE_TRUNC('week', publish_day)  AS publish_week,
    DATE_TRUNC('month', publish_day) AS publish_month,
    COUNT(DISTINCT id)               AS vacancies_count
FROM public.stg_vacancies
GROUP BY 1, 2, 3, 4, 5
