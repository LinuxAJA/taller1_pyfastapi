import re
from models import trainee_model
from templates import trainee_template

def validate_trainee_data(data):
    """
    Valida todos los campos de entrada de un aprendiz.
    Retorna (True, None) si todo es válido, o (False, "Mensaje de error").
    """
    errors = []
    # 1. Tipo de documento
    valid_doc_types = ["CC", "TI", "CE"]
    if data["tipo_doc"] not in valid_doc_types:
        errors.append(f"Tipo de documento inválido. Opciones válidas: {', '.join(valid_doc_types)}")

    # 2. Número de Documento (Solo dígitos)
    if not data["documento"].isdigit():
        errors.append("El número de documento debe contener únicamente dígitos numéricos.")

    # 3. Nombre Completo (No vacío y formato de texto)
    if len(data["nombre"]) < 3:
        errors.append("El nombre completo debe tener al menos 3 caracteres.")

    # 4. Número de Ficha (Solo dígitos)
    if not data["ficha"].isdigit():
        errors.append("El número de ficha debe ser numérico.")

    # 5. Programa de Formación (No vacío)
    if len(data["programa"]) < 3:
        errors.append("El nombre del programa de formación debe ser más descriptivo.")

    # 6. Correo Electrónico (Expresión regular estándar)
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, data["email"]):
        errors.append("El correo electrónico no tiene un formato válido (ejemplo: usuario@sena.edu.co).")

    if errors:
        return False, "\n".join(errors)

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
            "text": f"Validación fallida:\n{error_msg}"
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

def list_view():
    all_trainees = trainee_model.get_all()
    trainee_template.display_trainees_list(
        all_trainees, "Todos los Aprendices Registrados"
    )

def search_view():
    term = trainee_template.get_single_input(
        "🔍 Ingrese el nombre o número de ficha a buscar:"
    )
    results = trainee_model.search_by_name_or_group(term)
    trainee_template.display_trainees_list(
        results, f"Resultados de búsqueda para '{term}'"
    )

def edit_view():
    doc = trainee_template.get_single_input(
        "Ingrese el número de documento del aprendiz a editar:"
    )
    trainee = trainee_model.search_by_document(doc)

    if not trainee:
        trainee_template.display_message(
            {"type": "error", "text": "Aprendiz no encontrado."}
        )
        return

    updated_data = trainee_template.get_edit_input(trainee)

    # Validamos los datos combinados
    is_valid, error_msg = validate_trainee_data(updated_data)
    if not is_valid:
        trainee_template.display_message({"type": "error", "text": error_msg})
        return

    trainee_model.update_trainee(doc, updated_data)
    trainee_template.display_message(
        {"type": "success", "text": "Datos actualizados exitosamente."}
    )

def delete_view():
    doc = trainee_template.get_single_input(
        "Ingrese el número de documento del aprendiz a eliminar:"
    )
    trainee = trainee_model.search_by_document(doc)

    if not trainee:
        trainee_template.display_message(
            {"type": "error", "text": "Aprendiz no encontrado."}
        )
        return

    if trainee_template.confirm_action(
        f"¿Seguro que desea eliminar a {trainee['nombre']}?"
    ):
        trainee_model.delete_trainee(doc)
        trainee_template.display_message(
            {"type": "success", "text": "Aprendiz eliminado del sistema."}
        )
    else:
        trainee_template.display_message(
            {"type": "info", "text": "Operación cancelada."}
        )

def export_csv_view():
    success, result = trainee_model.export_to_csv()
    if success:
        trainee_template.display_message(
            {"type": "success", "text": f"Datos exportados a: {result}"}
        )
    else:
        trainee_template.display_message(
            {"type": "error", "text": f"Error al exportar: {result}"}
        )

def main_menu_controller():
    """Controlador principal que gestiona las opciones del menú."""
    init_app_data()

    while True:
        opcion = trainee_template.display_main_menu()

        if opcion == "1":
            register_trainee_view()
        elif opcion == "2":
            list_view()
        elif opcion == "3":
            search_view()
        elif opcion == "4":
            edit_view()
        elif opcion == "5":
            delete_view()
        elif opcion == "6":
            export_csv_view()
        elif opcion == "7":
            trainee_template.display_message(
                {"type": "info", "text": "¡Gracias por usar el sistema! Hasta luego."}
            )
            break
        else:
            trainee_template.display_message(
                {"type": "error", "text": "Opción no válida. Intente de nuevo."}
            )