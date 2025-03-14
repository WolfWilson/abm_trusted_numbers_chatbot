import sys
import getpass
from PyQt6.QtWidgets import QMessageBox
from Modules.conexion_db import verificar_permiso  # Importa la función que ejecuta el SP

def verificar_acceso():
    """
    Verifica si el usuario tiene permiso para ejecutar la aplicación.
    Llama al procedimiento almacenado 'Tiene_permiso'.
    """
    usuario = getpass.getuser()  # Obtiene el usuario actual
    grupo = "dominio\\GSP_CEL_ABM"  # Grupo autorizado

    # 🔹 Verifica si sys.stdout está disponible antes de imprimir
    def safe_print(msg):
        if sys.stdout:
            print(msg)
            sys.stdout.flush()  # Asegura que se imprima inmediatamente

    safe_print(f"🔍 Verificando permisos para el usuario '{usuario}' en el grupo '{grupo}'...")

    tiene_permiso = verificar_permiso(grupo)  # Llama al SP en la BD

    if tiene_permiso:
        safe_print(f"✅ Usuario '{usuario}' tiene permisos para ejecutar la aplicación.")
    else:
        safe_print(f"❌ Usuario '{usuario}' NO tiene permisos para ejecutar la aplicación.")
        
        # Muestra mensaje y cierra el programa
        QMessageBox.critical(None, "Acceso Denegado", 
                             "No tiene permisos para ejecutar esta aplicación.\n"
                             "Contacte al administrador.")
        sys.exit(0)  # Cierra la aplicación si no tiene acceso

