{{ config(
    tags=["staging"]
) }}

SELECT
    id_nb AS pokemon_id,  
    name,
    type_1,
    type_2,
    data_species,
    data_height AS height, 
    data_weight AS weight, 
    data_abilities AS abilities,
    training_catch_rate AS catch_rate,  
    training_base_exp AS base_experience,  
    training_growth_rate AS growth_rate,
    gender_male_pct, 
    gender_female_pct, 
    stats_hp AS hp,  
    stats_attack AS attack,  
    stats_defense AS defense,  
    stats_sp_atk AS special_attack,  
    stats_sp_def AS special_defense,  
    stats_speed AS speed,  
    stats_total AS total  
FROM {{ source('raw_data', 'pokemon_raw') }}