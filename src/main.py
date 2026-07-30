from views import trainee_view
from templates import trainee_template

def main():
    
    trainee_view.init_app_data()  # Inicializa los datos de la aplicación
    
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
    

#1. Refactorizar ruta del archivo JSON en la carpeta data/
#2. Refactorizar validaciones de los datos de entrada(incluir el correo electrónico) en la vista para que sean más robustas y claras.(Númerica, alfabética, correo electrónico, etc.)
#3. Implementar el editar de aprendices para permitir modificar los datos de un aprendiz existente.
#4. Implementar la eliminación de aprendices para permitir borrar un aprendiz existente de la lista.
#5. Implementar la búsqueda de aprendices por nombre o ficha para facilitar la localización de registros específicos.
#6. Implementar la exportación de la lista de aprendices a un archivo CSV para facilitar el manejo de datos fuera del programa.
#7. Implementar un menú principal para que el usuario pueda elegir entre registrar, editar, eliminar, buscar o exportar aprendices, en lugar de solo registrar uno tras otro.