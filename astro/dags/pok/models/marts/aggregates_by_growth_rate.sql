SELECT
    growth_rate,
    COUNT(*) AS pokemon_count,
    AVG(catch_rate) AS avg_catch_rate,
    AVG(base_experience) AS avg_base_exp,
    AVG(total) AS avg_stats_total
FROM {{ ref('stg_pokemon') }}
GROUP BY growth_rate