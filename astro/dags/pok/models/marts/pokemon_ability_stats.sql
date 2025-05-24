{{ config(
    tags=["mart"]
) }}
SELECT
    a.ability,
    COUNT(DISTINCT c.pokemon_id) AS pokemon_count,
    AVG(c.total) AS avg_stats_total,
    AVG(c.hp) AS avg_hp
FROM {{ ref('pokemon_abilities') }} a
JOIN {{ ref('stg_pokemon') }} c USING (pokemon_id)
GROUP BY a.ability
