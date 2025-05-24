{{ config(
    tags=["mart"]
) }}
SELECT
    type,
    is_primary_type,
    COUNT(*) AS count
FROM {{ ref('pokemon_types') }}
GROUP BY type, is_primary_type
ORDER BY type, is_primary_type DESC
