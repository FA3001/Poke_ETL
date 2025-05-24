{{ config(
    tags=["mart"]
) }}

SELECT
    catch_rate_group,
    COUNT(*) AS pokemon_count,
    AVG(total) AS avg_stats_total,
    AVG(hp) AS avg_hp
FROM {{ ref('catch_rate_group') }}
JOIN {{ ref('stg_pokemon') }} USING (pokemon_id)
GROUP BY catch_rate_group

