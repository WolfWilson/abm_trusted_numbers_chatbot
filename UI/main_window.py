from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QGridLayout
)
from Modules.conexion_db import buscar_por_dni
from Modules.styles import STYLE_MAIN_WINDOW

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABM Números de Confianza")
        self.setGeometry(100, 100, 500, 300)

        self.setStyleSheet(STYLE_MAIN_WINDOW)

        layout = QVBoxLayout()

        # Ingreso de DNI
        self.label_dni = QLabel("Ingrese DNI:")
        self.input_dni = QLineEdit()
        self.btn_buscar = QPushButton("Buscar")

        layout.addWidget(self.label_dni)
        layout.addWidget(self.input_dni)
        layout.addWidget(self.btn_buscar)

        # Grid para mostrar resultados
        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        # Etiquetas de datos (inicialmente vacías)
        self.labels = {
            "Nro_jub": QLabel("Número de Jubilación: "),
            "CUIL": QLabel("CUIL: "),
            "Nro_doc": QLabel("DNI: "),
            "Nombre": QLabel("Nombre: "),
            "Activo": QLabel("Activo: "),
            "Tipo_Benef": QLabel("Tipo de Beneficio: "),
            "telchatbot": QLabel("Teléfono: "),
            "principal": QLabel("Principal: "),
            "notificacion": QLabel("Notificación: "),
        }

        # Agregar etiquetas al grid layout
        row = 0
        for key, label in self.labels.items():
            self.grid_layout.addWidget(QLabel(f"{label.text()}"), row, 0)
            self.grid_layout.addWidget(label, row, 1)
            row += 1

        self.btn_buscar.clicked.connect(self.buscar_dni)

        self.setLayout(layout)

    def buscar_dni(self):
        dni = self.input_dni.text().strip()
        if dni.isdigit():
            resultado = buscar_por_dni(int(dni))
            if resultado:
                datos = resultado[0]  # Tomar el primer resultado
                for key, value in datos.items():
                    if key in self.labels:
                        self.labels[key].setText(str(value))  # Actualizar texto de etiquetas
            else:
                self.limpiar_labels("No se encontraron datos.")
        else:
            self.limpiar_labels("Ingrese un DNI válido.")

    def limpiar_labels(self, mensaje=""):
        """ Limpia las etiquetas o muestra un mensaje de error """
        for key in self.labels:
            self.labels[key].setText(mensaje)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
