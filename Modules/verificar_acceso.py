# Modules/verificar_acceso.py
import sys
import getpass
from PyQt6.QtWidgets import QApplication
from Modules.conexion_db import verificar_permiso
from Modules.denied_dialog import show_access_denied_dialog  # ⬅ Importamos nuestro módulo

def verificar_acceso():
    usuario = getpass.getuser()
    grupo = "dominio\\GSP_CEL_ABM"

    print(f"Verificando permisos para {usuario} en {grupo}...")
    # Podrías forzar a False para pruebas:
    # tiene_permiso = False
    # o la llamada real:
    tiene_permiso = verificar_permiso(grupo)

    if not tiene_permiso:
        show_access_denied_dialog()  # ⬅ Llamada a la ventana
    else:
        print("✅ Tiene permisos, puede continuar.")
