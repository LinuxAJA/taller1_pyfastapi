# Se importan las clases necesarias de FastAPI:
# - FastAPI: permite crear la aplicación web.
# - HTTPException: permite devolver errores HTTP personalizados.
from fastapi import FastAPI, APIRouter, HTTPException, status

from contextlib import asynccontextmanager

# Se importa la función que consume la API de Rick & Morty.
# Esta función obtiene un personaje aleatorio o uno específico según el ID recibido.
from services.rick_morty_api import get_random_character

# Se importa los modelos y views 
from models import trainee_model
from schemas.trainee_schema import TraineeCreate
from schemas.trainee_schema import TraineeUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Carga los aprendices desde el archivo JSON al iniciar la aplicacion"""
    trainee_model.load_from_json()
    yield

# Se crea una instancia de la aplicación FastAPI.
# La información proporcionada aparecerá en la documentación automática (/docs).
app = FastAPI(
    title="Rick and Morty Consumer and Trainee Service API",
    description="API simple con FastAPI para consumir la API de Rick & Morty",
    version="1.0.0",
    lifespan=lifespan
)

router = APIRouter(
    prefix="/character",
    tags=["Rick and Morty Character"]
)
# Se crean los endpoints necesarios

# Endpoint raíz de la API.
# Se accede escribiendo: http://localhost:8000/
@router.get("/")
def home():
    # Devuelve un mensaje de bienvenida en formato JSON.
    return {
        "message": "Bienvenido a la API de Rick & Morty con FastAPI. Visita /docs para ver la documentación interactiva."
    }


# Endpoint que obtiene un personaje aleatorio.
# URL: http://localhost:8000/character/random
@router.get("/random", summary="Leer Personaje Random")
async def read_random_character():
    """
    Endpoint para obtener un personaje completamente aleatorio.
    """

    # Llama a la función asíncrona que consulta la API externa.
    # Como la función es async, se utiliza await para esperar el resultado.
    character = await get_random_character()

    # Si la función devuelve None o un valor vacío,
    # significa que hubo un problema al consultar la API.
    if not character:
        raise HTTPException(
            status_code=500,
            detail="No se pudo obtener el personaje de la API externa."
        )

    # Devuelve el personaje en formato JSON.
    return character


# Endpoint para buscar un personaje por su ID.
# Ejemplo:
# http://localhost:8000/character/25
@router.get("/{character_id}", summary="Leer Personaje Por ID")
async def read_character_by_id(character_id: int):
    """
    Endpoint para obtener un personaje específico mediante su ID.
    """

    # Se valida que el ID esté dentro del rango existente
    # en la API de Rick & Morty.
    if character_id < 1 or character_id > 826:
        raise HTTPException(
            status_code=400,
            detail="El ID del personaje debe estar entre 1 y 826."
        )

    # Se llama a la función enviando el ID recibido.
    # La función buscará ese personaje específico.
    character = await get_random_character(character_id=character_id)

    # Si no existe un personaje con ese ID,
    # se devuelve un error 404 (No encontrado).
    if not character:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontró el personaje con ID {character_id}."
        )

    # Si todo salió bien, devuelve la información del personaje.
    return character

app.include_router(router)

# ======================================
# Endpoints de Sevicio Propio Aprendices
# ======================================


# Endpoint para ver aprendices
# URL = 
@app.get("/trainees/", tags=["Trainees"])
def get_all_trainnes():
    """ Endpoint para obtener todos los aprendices. """
    return trainee_model.get_all()

@app.post("/trainees/create/", tags=["Trainees"], status_code=status.HTTP_201_CREATED)
def post_new_trainee(trainee_data: TraineeCreate):
    """ Endpoint para crear nuevo aprendiz """
    trainee_dict = trainee_data.model_dump()
    return trainee_model.register_trainee(trainee_dict)

@app.get("/trainees/buscar/{criterio}", tags=["Trainees"])
def search_trainee(criterio: str):
    """ Endpoint para buscar aprendices por nombre o ficha """
    return trainee_model.search_by_name_or_group(criterio)

@app.put("/trainees/{trainee_id}", tags=["Trainees"])
def put_trainee(trainee_id: str, trainee_data: TraineeUpdate):
    """ Endpoint para editar aprendiz """
    trainee_dict = trainee_data.model_dump()
    return trainee_model.update_trainee(trainee_id, trainee_dict)

@app.delete("/trainees/{trainee_id}", tags=["Trainees"])
def delete_trainee(trainee_id: str):
    """ Endpoint para borrar aprendiz"""
    return trainee_model.delete_trainee(trainee_id)

@app.get("/trainee/export/csv", tags=["Trainees"])
def export_trainee_to_csv():
    """ Endpoint para exportar trainees.json a csv """
    return trainee_model.export_to_csv()
