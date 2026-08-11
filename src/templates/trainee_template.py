import textwrap

def display_main_menu():
    """ Muestra el menú principal y solicita una opción. """
    print(textwrap.dedent(f"""
            {"=" * 45}
            🎓 SISTEMA DE GESTIÓN DE APRENDICES SENA
            {"=" * 45}
            1. Registrar nuevo aprendiz
            2. Listar todos los aprendices
            3. Buscar aprendiz (por Nombre o Ficha)
            4. Editar aprendiz existente
            5. Eliminar aprendiz
            6. Exportar lista a CSV
            7. Salir
        """))
    return input("\nSeleccione una opción (1-7): ").strip()


def get_trainee_input():
    """ Solicita al usuario los datos del aprendiz incluyendo el correo. """
    print("\n--- 📝 REGISTRO DE APRENDIZ ---")
    type_id = input("Tipo de documento (CC/TI/CE): ").strip().upper()
    id = input("Número de documento: ").strip()
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

def get_single_input(prompt):
    """Solicita un único dato genérico (ej: para buscar o borrar)."""
    return input(f"\n{prompt} ").strip()


def get_edit_input(current_data):
    """Solicita los datos a editar. Si se presiona Enter, conserva el actual."""
    print("\n--- ✏️ EDITAR APRENDIZ ---")
    print("Deja el espacio en blanco y presiona Enter para mantener el valor actual.")

    type_id = (
        input(f"Tipo doc ({current_data['tipo_doc']}): ").strip().upper()
        or current_data["tipo_doc"]
    )
    name = (
        input(f"Nombre ({current_data['nombre']}): ").strip().title()
        or current_data["nombre"]
    )
    group_code = (
        input(f"Ficha ({current_data['ficha']}): ").strip() or current_data["ficha"]
    )
    program = (
        input(f"Programa ({current_data['programa']}): ").strip().title()
        or current_data["programa"]
    )
    email = (
        input(f"Email ({current_data['email']}): ").strip().lower()
        or current_data["email"]
    )

    return {
        "tipo_doc": type_id,
        "documento": current_data["documento"],
        "nombre": name,
        "ficha": group_code,
        "programa": program,
        "email": email,
    }


def confirm_action(prompt):
    return input(f"\n⚠️ {prompt} (s/n): ").strip().lower() == "s"

def display_message(message):
    icons = {"success": "✅ ", "error": "⚠️ ", "info": "ℹ️ "}
    print(f"\n{icons.get(message['type'], '')} {message['text']}")


def display_trainees_list(trainees_list, title="Lsita de Aprendices Registrados"):
    if not trainees_list:
        print("\nNo se encontraron aprendices registrados.")
        return

    print(f"\n--- {title} ---")
    for trai in trainees_list:
        print(
            f"Doc: {trai['tipo_doc']} {trai['documento']} | "
            f"Nombre: {trai['nombre']} | "
            f"Ficha: {trai['ficha']} | "
            f"Programa: {trai['programa']} | "
            f"Email: {trai['email']}"
        )