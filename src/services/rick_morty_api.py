import httpx
import random

API_BASE_URL = "https://rickandmortyapi.com/api"
API_CHARACTERS_ENDPOINT = f"{API_BASE_URL}/character"
API_EPISODES_ENDPOINT = f"{API_BASE_URL}/episode"
API_LOCATIONS_ENDPOINT = f"{API_BASE_URL}/location"

async def get_random_character(character_id: int = None):
    """Obtiene un personaje aleatorio de la API de Rick and Morty."""
    if character_id is None:
        random_id = random.randint(1, 826)  # Hay 826 personajes en la API
    else:
        random_id = character_id
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_CHARACTERS_ENDPOINT}/{random_id}", timeout=5.0)
            if (response.status_code != 200):
                return None
            
            data = response.json()
            return {
                "id": data["id"],
                "name": data["name"],
                "status": data["status"],
                "species": data["species"],
                "image": data["image"]
            }
    except Exception:
        pass
    
    return None