{{ config(materialized='view', schema='intermed', tags=["intermediate"]) }}
SELECT
    pokemon_id,
    name,
    CASE 
        WHEN catch_rate <= 50 THEN 'Low'
        WHEN catch_rate <= 150 THEN 'Medium'
        ELSE 'High'
    END AS catch_rate_group
FROM {{ ref('stg_pokemon') }}
