{{ config(materialized='view', schema='intermed') }}

SELECT
    pokemon_id,
    name,
    type_1 AS type,
    TRUE AS is_primary_type
FROM {{ ref('stg_pokemon') }}
WHERE type_1 IS NOT NULL

UNION ALL

SELECT
    pokemon_id,
    name,
    type_2 AS type,
    FALSE AS is_primary_type
FROM {{ ref('stg_pokemon') }}
WHERE type_2 IS NOT NULL