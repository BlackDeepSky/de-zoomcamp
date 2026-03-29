/*@bruin
name: public.mart_top_skills
type: pg.sql
connection: pg_local
materialization:
  type: table
  strategy: create+replace
depends_on:
  - public.stg_vacancies
@bruin*/

WITH unnested_skills AS (
    SELECT
        role_category,
        -- STRING_TO_ARRAY разбивает нашу строку обратно в массив, а UNNEST делает из массива строки
        TRIM(UNNEST(STRING_TO_ARRAY(skills, ','))) AS skill_name
    FROM public.stg_vacancies
    WHERE skills IS NOT NULL AND skills != ''
),
skill_counts AS (
    SELECT
        role_category,
        skill_name,
        COUNT(*) as skill_mentions
    FROM unnested_skills
    GROUP BY 1, 2
)
SELECT * FROM (
    SELECT
        role_category,
        skill_name,
        skill_mentions,
        -- Ранжируем навыки внутри каждой профессии
        ROW_NUMBER() OVER(PARTITION BY role_category ORDER BY skill_mentions DESC) as rank
    FROM skill_counts
) ranked
WHERE rank <= 5
