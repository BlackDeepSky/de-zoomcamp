/*@bruin
name: public.stg_vacancies
type: pg.sql
connection: pg_local
materialization:
  type: view
depends_on:
  - public.raw_vacancies
@bruin*/

SELECT
    id,
    role_category,
    title,
    employer,
    experience,
    skills,
    url,
    -- Превращаем ISO строку в нормальный Timestamp
    published_at::timestamptz AS published_date,
    DATE(published_at::timestamptz AT TIME ZONE 'Europe/Minsk') AS publish_day
FROM public.raw_vacancies
