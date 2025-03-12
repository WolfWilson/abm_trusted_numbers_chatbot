import sys
import getpass
from PyQt6.QtWidgets import QApplication, QMessageBox
from Modules.conexion_db import verificar_permiso  # Importa la función que ejecuta el SP

def verificar_acceso():
    """
    Verifica si el usuario tiene permiso para ejecutar la aplicación.
    Llama al procedimiento almacenado 'Tiene_permiso' en la base de datos.
    """
    usuario = getpass.getuser()  # Obtiene el usuario actual
    grupo = "dominio\\GSP_CEL_ABM"  # Grupo autorizado

    print(f"🔍 Verificando permisos para el usuario '{usuario}' en el grupo '{grupo}'...")
    sys.stdout.flush()

    tiene_permiso = verificar_permiso(grupo)  # Ejecuta el procedimiento almacenado

    if tiene_permiso:
        print(f"✅ Usuario '{usuario}' tiene permisos para ejecutar la aplicación.")
        sys.stdout.flush()
    else:
        print(f"❌ Usuario '{usuario}' NO tiene permisos para ejecutar la aplicación.")
        sys.stdout.flush()
        
        # Muestra mensaje de error y cierra la aplicación
        QMessageBox.critical(None, "Acceso Denegado", 
                             "No tiene permisos para ejecutar esta aplicación.\n"
                             "Contacte al administrador.")
        sys.exit(0)  # Cierra la aplicación si no tiene acceso

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Se inicializa la app para QMessageBox
    verificar_acceso()  # Llamada a la función de validación de permisos
    print("🚀 Prueba de permisos completada. El programa puede continuar ejecutándose.")
    sys.exit(app.exec())  # Se ejecuta el evento loop de la aplicación
