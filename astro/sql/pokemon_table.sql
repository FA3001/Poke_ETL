-- Create raw_pok schema
CREATE SCHEMA IF NOT EXISTS raw_pok;

CREATE TABLE IF NOT EXISTS raw_pok.pokemon_raw (
    id_nb INTEGER,
    name TEXT,
    type_1 TEXT,
    type_2 TEXT,
    data_species TEXT,
    data_height FLOAT,
    data_weight FLOAT,
    data_abilities TEXT,
    training_catch_rate INTEGER,
    training_base_exp INTEGER,
    training_growth_rate TEXT,
    gender_male_pct FLOAT,
    gender_female_pct FLOAT,
    stats_hp INTEGER,
    stats_attack INTEGER,
    stats_defense INTEGER,
    stats_sp_atk INTEGER,
    stats_sp_def INTEGER,
    stats_speed INTEGER,
    stats_total INTEGER
);
