import json
import os
# Base de datos en archivo JSON 
DATABASE_FILE = os.path.join(os.path.dirname(__file__),"trainees.json")

trainees = []

# Crea la carpeta data/ y el archivo trainees.json si no existen
def ensure_data_file_exists():
    """Asegura que el archivo de datos exista, creándolo si es necesario."""
    if not os.path.exists(DATABASE_FILE):
        os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
        with open(DATABASE_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)  # Inicializa con una lista vacía

def load_data():
    """Carga los datos de aprendices desde el archivo JSON."""
    global trainees
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r", encoding="utf-8") as file:
            try:
                trainees = json.load(file)
            except json.JSONDecodeError:
                trainees = []
    else:
        trainees = []
        
def save_data():
    """Guarda los datos de aprendices en el archivo JSON."""
    with open(DATABASE_FILE, "w", encoding="utf-8") as file:
        json.dump(trainees, file, ensure_ascii=False, indent=4)

def get_all():
    """Obtiene todos los aprendices registrados."""
    return trainees

def search_by_document(document):
    """Busca un aprendiz por su número de documento."""
    for a in trainees:
        if a["documento"] == document:
            return a
    return None

def register_trainee(new_trainee):
    """Registra un nuevo aprendiz si no existe previamente."""
    if search_by_document(new_trainee["documento"]):
        return False  # Ya existe un aprendiz con este documento
    trainees.append(new_trainee)
    save_data()
    return True