from views import trainee_view
from templates import trainee_template

def main():
    while True:
        # Registrar un aprendiz
        trainee_view.register_trainee_view()
        
        # Mostrar el estado actual de la lista de aprendices registrados
        trainee_view.status_view()
                
        # Preguntar si desea registrar otro aprendiz
        if not trainee_template.display_confirm_next():
            print("Saliendo del programa. ¡Hasta luego!")
            break
        
if __name__ == "__main__":
    main()