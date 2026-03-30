{{ config(materialized='table') }}

WITH unnested_skills AS (
    SELECT
        role_category,
        TRIM(UNNEST(STRING_TO_ARRAY(skills, ','))) AS skill_name
    FROM {{ source('public', 'stg_vacancies') }}
    WHERE skills IS NOT NULL AND skills != ''
),
skill_counts AS (
    SELECT
        role_category,
        skill_name,
        COUNT(*) AS skill_mentions
    FROM unnested_skills
    GROUP BY 1, 2
)
SELECT * FROM (
    SELECT
        role_category,
        skill_name,
        skill_mentions,
        ROW_NUMBER() OVER(PARTITION BY role_category ORDER BY skill_mentions DESC) AS rank
    FROM skill_counts
) ranked
WHERE rank <= 5
