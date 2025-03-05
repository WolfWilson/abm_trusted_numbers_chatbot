from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
)
from Modules.conexion_db import buscar_por_dni
from Modules.styles import STYLE_MAIN_WINDOW

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABM Números de Confianza")
        self.setGeometry(100, 100, 700, 400)
        self.setStyleSheet(STYLE_MAIN_WINDOW)

        layout = QVBoxLayout()

        # Ingreso de DNI
        self.label_dni = QLabel("Ingrese DNI:")
        self.input_dni = QLineEdit()
        self.btn_buscar = QPushButton("Buscar")

        layout.addWidget(self.label_dni)
        layout.addWidget(self.input_dni)
        layout.addWidget(self.btn_buscar)

        # Tabla para mostrar los resultados
        self.table = QTableWidget()
        self.table.setColumnCount(6)  # Número de columnas
        self.table.setHorizontalHeaderLabels([
            "CUIL", "Teléfono", "Principal", "Notificación", "Activo", "Tipo Benef."
        ])
        self.table.setColumnWidth(0, 130)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 90)
        self.table.setColumnWidth(3, 90)
        self.table.setColumnWidth(4, 70)
        self.table.setColumnWidth(5, 110)

        layout.addWidget(self.table)

        self.btn_buscar.clicked.connect(self.buscar_dni)

        self.setLayout(layout)

    def buscar_dni(self):
        dni = self.input_dni.text().strip()
        if dni.isdigit():
            resultado = buscar_por_dni(int(dni))
            self.mostrar_resultados(resultado)
        else:
            self.mostrar_resultados([])

    def mostrar_resultados(self, resultados):
        """ Muestra los resultados en la tabla """
        self.table.setRowCount(len(resultados))

        for row, data in enumerate(resultados):
            self.table.setItem(row, 0, QTableWidgetItem(str(data["CUIL"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(data["telefono"])))  # Teléfono dinámico
            self.table.setItem(row, 2, QTableWidgetItem("Sí" if data["principal"] else "No"))
            self.table.setItem(row, 3, QTableWidgetItem("Sí" if data["notificacion"] else "No"))
            self.table.setItem(row, 4, QTableWidgetItem(str(data["Activo"])))
            self.table.setItem(row, 5, QTableWidgetItem(str(data["Tipo_Benef"])))

        if not resultados:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("No hay datos"))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
