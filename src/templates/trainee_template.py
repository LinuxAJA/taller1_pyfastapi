def get_trainee_input():
    """Solicita al usuario los datos del aprendiz incluyendo el correo."""
    print("\n--- 📝 REGISTRO DE APRENDIZ ---")
    id = input("Número de documento: ").strip()
    type_id = input("Tipo de documento (CC/TI/CE): ").strip().upper()
    name = input("Nombre completo: ").strip().title()
    group_code = input("Número de Ficha: ").strip()
    program = input("Programa de Formación: ").strip().title()
    email = input("Correo electrónico: ").strip().lower()

    return {
        "tipo_doc": type_id,
        "documento": id,
        "nombre": name,
        "ficha": group_code,
        "programa": program,
        "email": email,
    }


def display_message(message):
    icons = {"success": "✅ ", "error": "⚠️ ", "info": "ℹ️ "}
    print(f"\n{icons.get(message['type'], '')} {message['text']}")


def display_trainees_list(trainees_list):
    if not trainees_list:
        print("\nNo hay aprendices registrados.")
        return

    print("\n--- Lista de Aprendices Registrados ---")
    for trai in trainees_list:
        print(
            f"Doc: {trai['tipo_doc']} {trai['documento']} | "
            f"Nombre: {trai['nombre']} | "
            f"Ficha: {trai['ficha']} | "
            f"Programa: {trai['programa']} | "
            f"Email: {trai['email']}"
        )


def display_confirm_next():
    """Pregunta al usuario si desea registrar otro aprendiz."""
    display_message({"type": "info", "text": "¿Deseas registrar otro aprendiz? (s/n)"})

    next = input("").strip().lower()
    return next == "s"