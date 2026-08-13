import json
import csv
from pathlib import Path

# Configuración dinámica de las rutas data, data/trainees.json, data/trainees.csv 
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "trainees.json"

CSV_FILE = DATA_DIR / "trainees.csv"

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

def update_trainee(document, updated_data):
    """ Actualiza los datos de un aprendiz existente """
    for i, a in enumerate(trainees):
        if a["documento"] == document:
            trainees[i].update(updated_data)
            save_to_json()
            return True
    return False

def delete_trainee(document):
    """ Elimina un Aprendiz por su Documento """
    global trainees
    initial_len = len(trainees)
    trainees = [a for a in trainees if a["documento"] != document]

    if len(trainees) != initial_len:
        save_to_json()
        return True
    return False

def search_by_name_or_group(term):
    """ Filtra aprendices cuyo nombre o ficha coincida parcialmente con el término. """
    term = term.lower()
    return [a for a in trainees if term in a["nombre"].lower() or term in a["ficha"]]

def export_to_csv():
    """ Exporta la lista actual a un archivo CSV. """
    if not trainees:
        return False, "No hay datos para exportar."

    try:
        with CSV_FILE.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=trainees[0].keys())
            writer.writeheader()
            writer.writerows(trainees)
        return True, str(CSV_FILE)
    except Exception as e:
        return False, str(e)