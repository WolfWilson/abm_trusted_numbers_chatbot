import sys
import getpass
from PyQt6.QtWidgets import QMessageBox
from Modules.conexion_db import verificar_permiso  # Función que ejecuta el SP

def verificar_acceso():
    """
    Verifica si el usuario tiene permiso para ejecutar la aplicación.
    Si el usuario es 'wbenitez', se le concede acceso automáticamente.
    """
    usuario = getpass.getuser()  # Obtiene el usuario actual
    grupo = "dominio\\GSP_CEL_ABM"  # Grupo autorizado

    # 🔹 Bypass para el usuario 'wbenitez'
    if usuario.lower() == "wbenitez":
        print(f"⚠ Usuario '{usuario}' forzado con acceso administrativo.")
        sys.stdout.flush()
        return  # Salta la verificación y permite ejecutar la aplicación

    # 🔹 Validación normal para otros usuarios
    tiene_permiso = verificar_permiso(grupo)

    if tiene_permiso:
        print(f"✅ Usuario '{usuario}' tiene permisos para ejecutar la aplicación.")
        sys.stdout.flush()
    else:
        print(f"❌ Usuario '{usuario}' NO tiene permisos para ejecutar la aplicación.")
        sys.stdout.flush()
        QMessageBox.critical(None, "Acceso Denegado", 
                             "No tiene permisos para ejecutar esta aplicación.\n"
                             "Contacte al administrador.")
        sys.exit(0)  # Cierra la aplicación si no tiene acceso
