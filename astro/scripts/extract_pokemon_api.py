import requests
import os
from datetime import datetime
import csv
import logging
from logging.handlers import RotatingFileHandler
from tenacity import retry, stop_after_attempt, wait_exponential
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler("data/api.log", maxBytes=1048576, backupCount=5)
logging.getLogger().addHandler(handler)

BASE_URL = "https://pokeapi.co/api/v2"
OUTPUT_DIR = "astro/data"

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def fetch_with_retry(url):
    """Fetch an API endpoint with retries."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def fetch_pokemon_data(pokemon_id):
    """Fetch data for a single Pokémon from PokeAPI."""
    try:
        # Fetch core Pokémon data
        pokemon = fetch_with_retry(f"{BASE_URL}/pokemon/{pokemon_id}")
        
        # Fetch species data
        species = fetch_with_retry(f"{BASE_URL}/pokemon-species/{pokemon_id}")
        
        # Extract types
        types = pokemon["types"]
        type_1 = types[0]["type"]["name"].capitalize() if types else None
        type_2 = types[1]["type"]["name"].capitalize() if len(types) > 1 else None
        
        # Extract abilities
        abilities = [a["ability"]["name"].capitalize() for a in pokemon["abilities"]]
        data_abilities = ", ".join(abilities) if abilities else None
        
        # Extract stats
        stats = {s["stat"]["name"]: s["base_stat"] for s in pokemon["stats"]}
        stats_total = sum(stats.values())
        
        # Extract gender percentages
        gender_rate = species.get("gender_rate", -1)  # -1 if genderless
        if gender_rate == -1:
            gender_male_pct = None
            gender_female_pct = None
        else:
            gender_female_pct = gender_rate * 12.5
            gender_male_pct = 100 - gender_female_pct
        
        # Extract species (genus)
        genera = next(
            (g["genus"] for g in species["genera"] if g["language"]["name"] == "en"),
            None
        )
        
        return {
            "id_nb": pokemon["id"],
            "name": pokemon["name"].capitalize(),
            "type_1": type_1,
            "type_2": type_2,
            "data_species": genera,
            "data_height": pokemon["height"] / 10.0,
            "data_weight": pokemon["weight"] / 10.0,
            "data_abilities": data_abilities,
            "training_catch_rate": species["capture_rate"],
            "training_base_exp": pokemon["base_experience"],
            "training_growth_rate": species["growth_rate"]["name"].replace("-", " ").title(),
            "gender_male_pct": gender_male_pct,
            "gender_female_pct": gender_female_pct,
            "stats_hp": stats.get("hp"),
            "stats_attack": stats.get("attack"),
            "stats_defense": stats.get("defense"),
            "stats_sp_atk": stats.get("special-attack"),
            "stats_sp_def": stats.get("special-defense"),
            "stats_speed": stats.get("speed"),
            "stats_total": stats_total
        }
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error for Pokémon {pokemon_id}: {e.response.status_code}")
        return None

def extract_pokemon_data(output_dir, limit):
    """Extract Pokémon data from PokeAPI and save to CSV."""
    pokemon_data = []
    
    # Fetch data in parallel
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(fetch_pokemon_data, range(1, limit + 1)))
    
    pokemon_data = [r for r in results if r is not None]
    logging.info(f"Fetched data for {len(pokemon_data)} Pokémon")
    
    # Define CSV fields (same as scraped dataset)
    fieldnames = [
        "id_nb", "name", "type_1", "type_2", "data_species", "data_height", "data_weight",
        "data_abilities", "training_catch_rate", "training_base_exp", "training_growth_rate",
        "gender_male_pct", "gender_female_pct", "stats_hp", "stats_attack", "stats_defense",
        "stats_sp_atk", "stats_sp_def", "stats_speed", "stats_total"
    ]
    
    # Write to CSV with timestamp
    # filename = f"pokemon_db_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    filename = f"pokemon_db.csv"
    csv_file = os.path.join(output_dir, filename)
    
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for pokemon in pokemon_data:
            writer.writerow(pokemon)
    
    logging.info(f"Data exported to {csv_file}")
    return csv_file

def main():
    csv_file = extract_pokemon_data(OUTPUT_DIR, 1008)
    print(f"Data exported to {csv_file}")

if __name__ == "__main__":
    main()