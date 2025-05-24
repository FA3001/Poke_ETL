{{ config(materialized='view', schema='intermed',tags=["intermediate"]) }}

SELECT
    pokemon_id,
    name,
    TRIM(UNNEST(STRING_TO_ARRAY(abilities, ','))) AS ability
FROM {{ ref('stg_pokemon') }}
WHERE abilities IS NOT NULL