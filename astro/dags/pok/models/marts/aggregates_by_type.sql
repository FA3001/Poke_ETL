SELECT
    type,
    COUNT(*) AS pokemon_count,
    AVG(total) AS avg_stats_total,
    AVG(hp) AS avg_hp,
    AVG(weight) AS avg_weight,
    AVG(height) AS avg_height
FROM {{ ref('pokemon_types') }}
JOIN {{ ref('stg_pokemon') }} USING (pokemon_id)
GROUP BY type