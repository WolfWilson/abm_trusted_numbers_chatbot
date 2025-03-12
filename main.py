from PyQt6.QtWidgets import QApplication
from UI.main_window import MainWindow
from Modules.verificar_acceso import verificar_acceso  # 🔹 Importamos la validación

if __name__ == "__main__":
    verificar_acceso()  # 🔹 Chequeo de permisos ANTES de abrir la ventana
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
