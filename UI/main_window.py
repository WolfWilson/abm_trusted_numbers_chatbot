from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QHBoxLayout, QComboBox
)
from PyQt6.QtGui import QGuiApplication  # ✅ Importación correcta
from Modules.conexion_db import buscar_por_dni
from Modules.styles import STYLE_MAIN_WINDOW

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABM Números de Confianza")
        self.setFixedSize(800, 400)  # Tamaño fijo de la ventana
        self.centrar_ventana()  # ✅ Llamada correcta a la función
        self.setStyleSheet(STYLE_MAIN_WINDOW)

        layout = QVBoxLayout()

        # Zona de búsqueda
        self.label_dni = QLabel("Ingrese DNI:")
        self.input_dni = QLineEdit()
        self.btn_buscar = QPushButton("Buscar")

        layout.addWidget(self.label_dni)
        layout.addWidget(self.input_dni)
        layout.addWidget(self.btn_buscar)

        # Tabla para mostrar resultados
        self.table = QTableWidget()
        self.table.setColumnCount(6)  
        self.table.setHorizontalHeaderLabels([
            "CUIL", "Teléfono", "Principal", "Notificación", "Estado", "Beneficio"
        ])
        self.table.setColumnWidth(0, 130)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 90)
        self.table.setColumnWidth(3, 90)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 200)

        layout.addWidget(self.table)

        # Sección para agregar un nuevo número
        self.label_agregar = QLabel("Agregar Nuevo Número")
        layout.addWidget(self.label_agregar)

        form_layout = QHBoxLayout()

        # Inputs para agregar número
        self.input_pais = QLineEdit()
        self.input_pais.setPlaceholderText("Cód. País")
        self.input_area = QLineEdit()
        self.input_area.setPlaceholderText("Cód. Área")
        self.input_numero = QLineEdit()
        self.input_numero.setPlaceholderText("Número Celular")
        self.input_referencia = QLineEdit()
        self.input_referencia.setPlaceholderText("Referencia (Máx 50)")

        # Etiquetas de Principal y Notificación
        self.label_principal = QLabel("Principal:")
        self.label_notificacion = QLabel("Notificación:")

        # Opciones Principal (Sí/No)
        self.combo_principal = QComboBox()
        self.combo_principal.addItems(["Sí", "No"])

        # Opciones Notificación (Sí/No)
        self.combo_notificacion = QComboBox()
        self.combo_notificacion.addItems(["Sí", "No"])

        # Botón para confirmar la adición
        self.btn_agregar = QPushButton("Agregar Número")

        # Agregar elementos al layout de formulario
        form_layout.addWidget(self.input_pais)
        form_layout.addWidget(self.input_area)
        form_layout.addWidget(self.input_numero)
        form_layout.addWidget(self.input_referencia)

        # Sub-layout para opciones Principal y Notificación
        opciones_layout = QVBoxLayout()
        opciones_layout.addWidget(self.label_principal)
        opciones_layout.addWidget(self.combo_principal)
        opciones_layout.addWidget(self.label_notificacion)
        opciones_layout.addWidget(self.combo_notificacion)

        form_layout.addLayout(opciones_layout)
        form_layout.addWidget(self.btn_agregar)

        layout.addLayout(form_layout)

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
        """ Muestra los resultados en la tabla con formato corregido """
        self.table.setRowCount(len(resultados))

        for row, data in enumerate(resultados):
            self.table.setItem(row, 0, QTableWidgetItem(str(data["CUIL"])))
            self.table.setItem(row, 1, QTableWidgetItem(str(data["telefono"])))
            self.table.setItem(row, 2, QTableWidgetItem("Sí" if data["principal"] else "No"))
            self.table.setItem(row, 3, QTableWidgetItem("Sí" if data["notificacion"] else "No"))
            self.table.setItem(row, 4, QTableWidgetItem("Activo" if data["Activo"] == 0 else "Inactivo"))
            self.table.setItem(row, 5, QTableWidgetItem(self.get_tipo_beneficio(data["Tipo_Benef"])))

        if not resultados:
            self.table.setRowCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("No hay datos"))

    def get_tipo_beneficio(self, tipo):
        """ Convierte el tipo de beneficio a su descripción """
        tipos = {
            0: "Haberes Impagos",
            1: "Pensión",
            2: "Jubilación",
            3: "Ley 5496",
            4: "Ley 5495",
            5: "Ex Combatiente de Malvinas",
            6: "Movilizados de Malvinas"
        }
        return tipos.get(tipo, "Desconocido")

    def centrar_ventana(self):
        """ Centra la ventana en la pantalla correctamente en PyQt6 """
        pantalla = QGuiApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(pantalla.center())
        self.move(ventana.topLeft())

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
