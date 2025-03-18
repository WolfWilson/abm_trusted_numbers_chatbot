# main.py
import sys
from PyQt6.QtWidgets import QApplication
from UI.main_window import MainWindow
from Modules.verificar_acceso import verificar_acceso  # Tu lógica de permisos

if __name__ == "__main__":
    app = QApplication(sys.argv)

    verificar_acceso()  # Si no hay permisos, se mostrará la ventana denied y se cierra.

    # Si llegamos aquí, es que sí hay permisos
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
