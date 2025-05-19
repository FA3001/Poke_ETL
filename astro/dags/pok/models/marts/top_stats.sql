
SELECT
    r.stat_type,
    r.pokemon_id,
    r.name,
    c.type_1,
    r.stat_value,
    r.stat_rank,
    c.total
FROM {{ ref('pokemon_stat_ranks') }} r
JOIN {{ ref('stg_pokemon') }} c USING (pokemon_id)
WHERE r.stat_rank <= 5  