
{{ config(materialized='view', schema='intermed') }}

SELECT pokemon_id, name, 'HP' AS stat_type, hp AS stat_value
FROM {{ ref('stg_pokemon') }}
UNION ALL
SELECT pokemon_id, name, 'Attack' AS stat_type, attack AS stat_value
FROM {{ ref('stg_pokemon') }}
UNION ALL
SELECT pokemon_id, name, 'Defense' AS stat_type, defense AS stat_value
FROM {{ ref('stg_pokemon') }}
UNION ALL
SELECT pokemon_id, name, 'Special Attack' AS stat_type, special_attack AS stat_value
FROM {{ ref('stg_pokemon') }}
UNION ALL
SELECT pokemon_id, name, 'Special Defense' AS stat_type, special_defense AS stat_value
FROM {{ ref('stg_pokemon') }}
UNION ALL
SELECT pokemon_id, name, 'Speed' AS stat_type, speed AS stat_value
FROM {{ ref('stg_pokemon') }}