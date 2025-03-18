# Modules/verificar_acceso.py
import sys
import getpass
from Modules.denied_dialog import show_access_denied_dialog  # Importa tu ventana "denied"
# from Modules.conexion_db import verificar_permiso  # Comenta esta línea si no la usarás

def verificar_acceso():
    usuario = getpass.getuser()
    grupo = "dominio\\GSP_CEL_ABM"

    print(f"Verificando permisos para {usuario} en {grupo}...")
    
    # Forzamos NO permiso para pruebas
    tiene_permiso = False

    if not tiene_permiso:
        show_access_denied_dialog()
    else:
        print("✅ Tiene permisos, puede continuar.")
