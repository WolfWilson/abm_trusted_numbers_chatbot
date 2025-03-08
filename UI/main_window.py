# UI/main_window.py

import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QHBoxLayout, QComboBox, QToolButton, QMessageBox, QHeaderView
)
from PyQt6.QtGui import QGuiApplication, QIcon, QPixmap, QPalette, QBrush
from PyQt6.QtCore import QSize, Qt

from Modules.conexion_db import buscar_por_dni
from Modules.styles import STYLE_MAIN_WINDOW
# Importamos nuestro módulo para insertar números
from Modules import add_number

def cargar_icono(nombre):
    ruta_base = os.path.abspath(os.path.dirname(__file__))
    ruta_icono = os.path.join(ruta_base, "..", "assets", nombre)
    return QIcon(ruta_icono)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABM Números de Confianza")
        self.setFixedSize(1000, 600)  
        self.centrar_ventana()

        # Icono de la ventana
        self.setWindowIcon(cargar_icono("phone.png"))

        # Estilos
        self.setStyleSheet(STYLE_MAIN_WINDOW)

        # Fondo de pantalla (opcional)
        self.aplicar_fondo_ventana()

        # Variable para almacenar el CUIL actual
        self.current_cuil = None

        layout = QVBoxLayout()

        # Zona de búsqueda
        self.label_dni = QLabel("Ingrese DNI:")
        self.label_dni.setObjectName("labelDni")
        self.input_dni = QLineEdit()
        self.btn_buscar = QPushButton("Buscar")

        layout.addWidget(self.label_dni)
        layout.addWidget(self.input_dni)
        layout.addWidget(self.btn_buscar)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Nombre", "Referencia", "Teléfono", "Principal", 
            "Notificación", "Estado", "Beneficio", "Editar", "Eliminar"
        ])
        layout.addWidget(self.table)

        # Label "Agregar Nuevo Número"
        self.label_agregar = QLabel("Agregar Nuevo Número")
        self.label_agregar.setObjectName("labelAgregar")
        layout.addWidget(self.label_agregar)

        # Sección para agregar un nuevo número
        form_layout = QHBoxLayout()
        self.input_pais = QLineEdit()
        self.input_pais.setPlaceholderText("Cód. País")
        self.input_area = QLineEdit()
        self.input_area.setPlaceholderText("Cód. Área")
        self.input_numero = QLineEdit()
        self.input_numero.setPlaceholderText("Número Celular")
        self.input_referencia = QLineEdit()
        self.input_referencia.setPlaceholderText("Referencia (Máx 50)")

        self.label_principal = QLabel("Principal:")
        self.label_principal.setObjectName("labelPrincipal")

        self.label_notificacion = QLabel("Notificación:")
        self.label_notificacion.setObjectName("labelNotificacion")

        self.combo_principal = QComboBox()
        self.combo_principal.addItems(["Sí", "No"])

        self.combo_notificacion = QComboBox()
        self.combo_notificacion.addItems(["Sí", "No"])

        # Botón "Agregar"
        self.btn_agregar = QToolButton()
        self.btn_agregar.setIcon(cargar_icono("add1.png"))
        self.btn_agregar.setToolTip("Agregar nuevo número")
        self.btn_agregar.setIconSize(QSize(60, 60))
        self.btn_agregar.setFixedSize(80, 50)

        # Armado del layout
        form_layout.addWidget(self.input_pais)
        form_layout.addWidget(self.input_area)
        form_layout.addWidget(self.input_numero)
        form_layout.addWidget(self.input_referencia)

        opciones_layout = QVBoxLayout()
        opciones_layout.addWidget(self.label_principal)
        opciones_layout.addWidget(self.combo_principal)
        opciones_layout.addWidget(self.label_notificacion)
        opciones_layout.addWidget(self.combo_notificacion)

        form_layout.addLayout(opciones_layout)
        form_layout.addWidget(self.btn_agregar)

        layout.addLayout(form_layout)

        # Conexiones
        self.btn_buscar.clicked.connect(self.buscar_dni)
        self.btn_agregar.clicked.connect(self.on_agregar_numero)

        self.setLayout(layout)

    def aplicar_fondo_ventana(self):
        ruta_base = os.path.abspath(os.path.dirname(__file__))
        ruta_imagen = os.path.join(ruta_base, "..", "assets", "bg.png")

        if os.path.exists(ruta_imagen):
            pixmap = QPixmap(ruta_imagen).scaled(
                self.width(), self.height(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            paleta = self.palette()
            paleta.setBrush(self.backgroundRole(), QBrush(pixmap))
            self.setPalette(paleta)
            self.setAutoFillBackground(True)
        else:
            print("⚠ No se encontró 'bg.png'. Se usará el fondo de estilo por defecto.")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.aplicar_fondo_ventana()

    def buscar_dni(self):
        dni = self.input_dni.text().strip()
        if dni.isdigit():
            resultado = buscar_por_dni(int(dni))
            self.mostrar_resultados(resultado)
        else:
            self.mostrar_resultados([])

    def mostrar_resultados(self, resultados):
        """
        Muestra: [Nombre, referencia, telefono, principal, notificación, estado, beneficio].
        Guarda el primer CUIL encontrado en self.current_cuil.
        """
        self.table.setRowCount(len(resultados))
        self.current_cuil = None  # Limpiamos el CUIL anterior

        for row, data in enumerate(resultados):
            # Guardar el primer CUIL
            if row == 0:
                self.current_cuil = data.get("CUIL")

            self.table.setItem(row, 0, QTableWidgetItem(str(data.get("Nombre", ""))))
            self.table.setItem(row, 1, QTableWidgetItem(str(data.get("referencia", ""))))
            self.table.setItem(row, 2, QTableWidgetItem(str(data.get("telefono", ""))))
            self.table.setItem(row, 3, QTableWidgetItem("Sí" if data.get("principal", 0) else "No"))
            self.table.setItem(row, 4, QTableWidgetItem("Sí" if data.get("notificacion", 0) else "No"))

            activo = "Activo" if data.get("Activo", 1) == 0 else "Inactivo"
            self.table.setItem(row, 5, QTableWidgetItem(activo))

            # 'Tipo_Benef' ya viene como texto, ej. 'Jubilación / Pensión'
            self.table.setItem(row, 6, QTableWidgetItem(str(data.get("Tipo_Benef", ""))))

            # Botones Editar / Eliminar (proximamente)
            btn_editar = QToolButton()
            btn_editar.setIcon(cargar_icono("edit1.png"))
            btn_editar.setIconSize(QSize(30, 30))
            btn_editar.setToolTip("Editar número")
            btn_editar.clicked.connect(lambda _, r=row: self.confirmar_accion("Editar", r))

            btn_eliminar = QToolButton()
            btn_eliminar.setIcon(cargar_icono("delete1.png"))
            btn_eliminar.setIconSize(QSize(30, 30))
            btn_eliminar.setToolTip("Eliminar número")
            btn_eliminar.clicked.connect(lambda _, r=row: self.confirmar_accion("Eliminar", r))

            self.table.setCellWidget(row, 7, btn_editar)
            self.table.setCellWidget(row, 8, btn_eliminar)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def on_agregar_numero(self):
        """
        1) Mensaje de confirmación antes de insertar
        2) Insertar con add_number.agregar_numero_confianza
        3) Refrescar la búsqueda
        4) Limpiar campos
        """
        if not self.current_cuil:
            QMessageBox.warning(self, "Error", "No hay CUIL seleccionado. Realice una búsqueda primero.")
            return

        pais = self.input_pais.text().strip()
        area = self.input_area.text().strip()
        abonado = self.input_numero.text().strip()
        referencia = self.input_referencia.text().strip()
        principal = 1 if self.combo_principal.currentText() == "Sí" else 0
        notificacion = 1 if self.combo_notificacion.currentText() == "Sí" else 0

        if not pais or not area or not abonado:
            QMessageBox.warning(self, "Datos incompletos", "Complete país, área y número.")
            return

        # 1) Mensaje de confirmación
        confirm_msg = f"¿Está seguro que desea agregar el número:\n" \
                      f"{pais} {area} {abonado}\n" \
                      f"para este beneficiario?"
        reply = QMessageBox.question(self, "Confirmar Alta", confirm_msg,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return  # No inserta

        # 2) Insertar
        resultado = add_number.agregar_numero_confianza(
            cuil=self.current_cuil,
            pais=pais,
            area=area,
            abonado=abonado,
            referencia=referencia,
            principal=principal,
            notificacion=notificacion
        )

        # 3) Refrescar la búsqueda (usamos el mismo DNI)
        self.buscar_dni()

        # 4) Limpiar campos
        self.input_pais.clear()
        self.input_area.clear()
        self.input_numero.clear()
        self.input_referencia.clear()
        self.combo_principal.setCurrentIndex(0)
        self.combo_notificacion.setCurrentIndex(0)

        # Mostrar mensaje final
        QMessageBox.information(self, "Agregar Número", resultado)

    def confirmar_accion(self, accion, row):
        mensaje = f"¿Está seguro que desea {accion.lower()} este número?"
        reply = QMessageBox.question(self, f"{accion} Número", mensaje,
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            print(f"{accion} número en fila {row}")
            # Aquí iría la lógica de edición/eliminación

    def centrar_ventana(self):
        pantalla = QGuiApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(pantalla.center())
        self.move(ventana.topLeft())


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
