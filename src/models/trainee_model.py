import json
from pathlib import Path

# Configuración dinámica de la ruta absoluta a data/aprendices.json
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "trainees.json"

trainees = []

def ensure_data_file_exists():
    """Garantiza la existencia de la carpeta data y el archivo JSON."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

def load_from_json():
    """Carga los aprendices guardados en el archivo JSON."""
    global trainees
    ensure_data_file_exists()
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            trainees = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        trainees = []
    return trainees

def save_to_json():
    """Guarda los aprendices en el archivo JSON."""
    ensure_data_file_exists()
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(trainees, f, ensure_ascii=False, indent=4)

def get_all():
    return trainees

def search_by_document(document):
    for a in trainees:
        if a["documento"] == document:
            return a
    return None

def register_trainee(new_trainee):
    if search_by_document(new_trainee["documento"]):
        return False
    trainees.append(new_trainee)
    save_to_json()
    return True