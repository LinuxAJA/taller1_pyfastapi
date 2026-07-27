# Capa TEMPLATE: Interfaz de usuario por consola para registrar aprendices


def get_trainee_input():
    """Solicita al usuario los datos para registrar un aprendiz."""
    id = input("Número de documento: ").strip()
    type_id = input("Tipo de documento (CC/TI/CE): ").strip().upper()
    name = input("Nombre completo: ").strip().title()
    group_code = input("Número de Ficha: ").strip()
    program = input("Programa de Formación: ").strip().title()

    return {
        "tipo_doc": type_id,
        "documento": id,
        "nombre": name,
        "ficha": group_code,
        "programa": program,
    }


def display_message(message):
    icons = {"success": "✅ ", "error": "⚠️ ", "info": "ℹ️ "}
    print(f"{icons.get(message['type'], '')} {message['text']}")


def display_trainee_list(trainee):
    """Muestra la lista de aprendices registrados."""
    if not trainee:
        print("No hay aprendices registrados.")
        return

    print("\n--- Lista de Aprendices Registrados ---")
    for trai in trainee:
        print(
            f"Documento: {trai['documento']}, Nombre: {trai['nombre']}, Ficha: {trai['ficha']}, Programa: {trai['programa']}"
        )


def display_confirm_next():
    """Pregunta al usuario si desea registrar otro aprendiz."""
    display_message({"type": "info", "text": "¿Deseas registrar otro aprendiz? (s/n)"})

    next = input("").strip().lower()
    return next == "s"
