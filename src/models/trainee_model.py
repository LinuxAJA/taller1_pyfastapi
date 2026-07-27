# Base de datos en memoria (Lista vacía al inicio)
trainee = []

def get_all():
    """Obtiene todos los aprendices registrados."""
    return trainee

def search_by_document(document):
    """Busca un aprendiz por su número de documento."""
    for a in trainee:
        if a["documento"] == document:
            return a
    return None

def register_trainee(new_trainee):
    """Registra un nuevo aprendiz si no existe previamente."""
    if search_by_document(new_trainee["documento"]):
        return False  # Ya existe un aprendiz con este documento
    trainee.append(new_trainee)
    return True