{{ config(materialized='view', schema='intermed') }}

SELECT
    pokemon_id,
    name,
    stat_type,
    stat_value,
    RANK() OVER (PARTITION BY stat_type ORDER BY stat_value DESC) AS stat_rank
FROM {{ ref('pokemon_stats') }}