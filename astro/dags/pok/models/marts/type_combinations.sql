SELECT
    type_1,
    type_2,
    CASE
        WHEN type_2 IS NOT NULL THEN type_1 || '/' || type_2
        ELSE type_1
    END AS type_combination,
    COUNT(*) AS pokemon_count,
    AVG(total) AS avg_stats_total
FROM {{ ref('stg_pokemon') }}
GROUP BY type_1, type_2