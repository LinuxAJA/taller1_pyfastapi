import re
from models import trainee_model
from templates import trainee_template

def validate_trainee_data(data):
    """
    Valida todos los campos de entrada de un aprendiz.
    Retorna (True, None) si todo es válido, o (False, "Mensaje de error").
    """
    # 1. Tipo de documento
    valid_doc_types = ["CC", "TI", "CE"]
    if data["tipo_doc"] not in valid_doc_types:
        return False, f"Tipo de documento inválido. Opciones válidas: {', '.join(valid_doc_types)}"

    # 2. Número de Documento (Solo dígitos)
    if not data["documento"].isdigit():
        return False, "El número de documento debe contener únicamente dígitos numéricos."

    # 3. Nombre Completo (No vacío y formato de texto)
    if len(data["nombre"]) < 3:
        return False, "El nombre completo debe tener al menos 3 caracteres."

    # 4. Número de Ficha (Solo dígitos)
    if not data["ficha"].isdigit():
        return False, "El número de ficha debe ser numérico."

    # 5. Programa de Formación (No vacío)
    if len(data["programa"]) < 3:
        return False, "El nombre del programa de formación debe ser más descriptivo."

    # 6. Correo Electrónico (Expresión regular estándar)
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, data["email"]):
        return False, "El correo electrónico no tiene un formato válido (ejemplo: usuario@sena.edu.co)."

    return True, None


def init_app_data():
    trainee_model.load_from_json()


def register_trainee_view():
    """Lógica principal del registro con capa de validación integrada."""
    data = trainee_template.get_trainee_input()
    
    # Validar formato y tipos de datos recibidos
    is_valid, error_msg = validate_trainee_data(data)
    if not is_valid:
        trainee_template.display_message({
            "type": "error",
            "text": f"Validación fallida: {error_msg}"
        })
        return

    # Validar duplicados en el Modelo
    if trainee_model.search_by_document(data["documento"]):
        trainee_template.display_message({
            "type": "error",
            "text": "Ya existe un aprendiz registrado con este número de documento."
        })
        return
    
    # Registrar aprendiz
    trainee_model.register_trainee(data)
    
    # Confirmar en la interfaz
    trainee_template.display_message({
        "type": "success",
        "text": f"Aprendiz {data['nombre']} registrado exitosamente con el correo {data['email']}."
    })


def status_view():
    all_trainees = trainee_model.get_all()
    trainee_template.display_trainees_list(all_trainees)