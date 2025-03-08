import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, 
    QTableWidgetItem, QHBoxLayout, QComboBox, QToolButton, QMessageBox, QHeaderView
)
from PyQt6.QtGui import QGuiApplication, QIcon, QPixmap, QPalette, QBrush
from PyQt6.QtCore import QSize, Qt

from Modules.conexion_db import buscar_por_dni
from Modules.styles import STYLE_MAIN_WINDOW
from Modules import add_number
from Modules import delete_number

def cargar_icono(nombre):
    ruta_base = os.path.abspath(os.path.dirname(__file__))
    ruta_icono = os.path.join(ruta_base, "..", "assets", nombre)
    return QIcon(ruta_icono)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABM Números de Confianza")
        self.setFixedSize(1020, 500)
        self.centrar_ventana()

        # Icono y estilos
        self.setWindowIcon(cargar_icono("phone.png"))
        self.setStyleSheet(STYLE_MAIN_WINDOW)
        self.aplicar_fondo_ventana()

        # Variable para almacenar el CUIL actual tras la búsqueda
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
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "idcelular (oculto)", "Nombre", "Referencia", "Teléfono", 
            "Principal", "Notificación", "Estado", "Beneficio", 
            "Editar", "Eliminar"
        ])
        self.table.setColumnHidden(0, True)  # Ocultamos el idcelular

        # Permitir dos líneas máximo si el texto es largo
        self.table.setWordWrap(True)
        # No redimensionar automáticamente. 
        # El usuario puede arrastrar si quiere.
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Anchos fijos iniciales para cada columna (ajusta a tu gusto)
        self.table.setColumnWidth(1, 160)  # Nombre
        self.table.setColumnWidth(2, 160)  # Referencia
        self.table.setColumnWidth(3, 130)  # Teléfono
        self.table.setColumnWidth(4, 80)   # Principal
        self.table.setColumnWidth(5, 100)  # Notificación
        self.table.setColumnWidth(6, 80)   # Estado
        self.table.setColumnWidth(7, 120)  # Beneficio
        self.table.setColumnWidth(8, 70)   # Editar
        self.table.setColumnWidth(9, 70)   # Eliminar

        # Forzar altura fija de cada fila (~ 2 líneas)
        self.table.verticalHeader().setDefaultSectionSize(40)

        layout.addWidget(self.table)

        # Sección "Agregar Nuevo Número"
        self.label_agregar = QLabel("Agregar Nuevo Número")
        self.label_agregar.setObjectName("labelAgregar")
        layout.addWidget(self.label_agregar)

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

        self.btn_agregar = QToolButton()
        self.btn_agregar.setIcon(cargar_icono("add1.png"))
        self.btn_agregar.setToolTip("Agregar nuevo número")
        self.btn_agregar.setIconSize(QSize(60, 60))
        self.btn_agregar.setFixedSize(80, 50)

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
        col0 -> idcelular
        col1 -> Nombre (2 líneas máximo, luego recorta)
        col2 -> Referencia
        col3 -> Telefono
        col4 -> Principal
        col5 -> Notificación
        col6 -> Estado
        col7 -> Beneficio
        col8 -> Editar
        col9 -> Eliminar
        """
        self.table.setRowCount(len(resultados))
        self.current_cuil = None

        for row, data in enumerate(resultados):
            if row == 0:
                self.current_cuil = data.get("CUIL", None)

            idcel = data.get("idcelular", "")
            item_id = QTableWidgetItem(str(idcel))
            self.table.setItem(row, 0, item_id)

            # Nombre
            nombre_text = str(data.get("Nombre", ""))
            item_nombre = QTableWidgetItem(nombre_text)
            # Tooltip para ver todo el texto
            item_nombre.setToolTip(nombre_text)
            # Se recortará a 2 líneas por la altura fija de 40 px
            self.table.setItem(row, 1, item_nombre)

            # Referencia
            referencia_text = str(data.get("referencia", ""))
            item_ref = QTableWidgetItem(referencia_text)
            item_ref.setToolTip(referencia_text)
            self.table.setItem(row, 2, item_ref)

            # Teléfono
            self.table.setItem(row, 3, QTableWidgetItem(str(data.get("telefono", ""))))

            # Principal
            principal_text = "Sí" if data.get("principal", 0) else "No"
            self.table.setItem(row, 4, QTableWidgetItem(principal_text))

            # Notificación
            notif_text = "Sí" if data.get("notificacion", 0) else "No"
            self.table.setItem(row, 5, QTableWidgetItem(notif_text))

            # Estado
            activo_val = data.get("Activo", 1)
            activo_text = "Activo" if activo_val == 0 else "Inactivo"
            self.table.setItem(row, 6, QTableWidgetItem(activo_text))

            # Beneficio
            self.table.setItem(row, 7, QTableWidgetItem(str(data.get("Tipo_Benef", ""))))

            # Botón Editar
            btn_editar = QToolButton()
            btn_editar.setIcon(cargar_icono("edit1.png"))
            btn_editar.setIconSize(QSize(30, 30))
            btn_editar.setToolTip("Editar número")
            btn_editar.clicked.connect(lambda _, r=row: self.confirmar_accion("Editar", r))

            # Botón Eliminar
            btn_eliminar = QToolButton()
            btn_eliminar.setIcon(cargar_icono("delete1.png"))
            btn_eliminar.setIconSize(QSize(30, 30))
            btn_eliminar.setToolTip("Eliminar número")
            btn_eliminar.clicked.connect(lambda _, r=row: self.confirmar_accion("Eliminar", r))

            self.table.setCellWidget(row, 8, btn_editar)
            self.table.setCellWidget(row, 9, btn_eliminar)

        # No llamamos a "resizeColumnsToContents" ni "resizeRowsToContents"
        # para mantener anchos y alturas fijos.

    def on_agregar_numero(self):
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

        # Confirmación
        confirm_msg = f"¿Está seguro que desea agregar el número:\n" \
                      f"{pais} {area} {abonado}\n" \
                      f"para este beneficiario?"
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmar Alta")
        msg_box.setText(confirm_msg)
        msg_box.setIcon(QMessageBox.Icon.Question)
        btn_si = msg_box.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        btn_no = msg_box.addButton("No", QMessageBox.ButtonRole.NoRole)
        msg_box.exec()

        if msg_box.clickedButton() == btn_no:
            return

        resultado = add_number.agregar_numero_confianza(
            cuil=self.current_cuil,
            pais=pais,
            area=area,
            abonado=abonado,
            referencia=referencia,
            principal=principal,
            notificacion=notificacion
        )

        self.buscar_dni()

        # Limpiar
        self.input_pais.clear()
        self.input_area.clear()
        self.input_numero.clear()
        self.input_referencia.clear()
        self.combo_principal.setCurrentIndex(0)
        self.combo_notificacion.setCurrentIndex(0)

        QMessageBox.information(self, "Agregar Número", resultado)

    def confirmar_accion(self, accion, row):
        mensaje = f"¿Está seguro que desea {accion.lower()} este número?"
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(f"{accion} Número")
        msg_box.setText(mensaje)
        msg_box.setIcon(QMessageBox.Icon.Question)
        btn_si = msg_box.addButton("Sí", QMessageBox.ButtonRole.YesRole)
        btn_no = msg_box.addButton("No", QMessageBox.ButtonRole.NoRole)
        msg_box.exec()

        if msg_box.clickedButton() == btn_no:
            return

        if accion == "Eliminar":
            idcel_item = self.table.item(row, 0)
            if not idcel_item:
                QMessageBox.warning(self, "Error", "No se encontró idcelular en la tabla.")
                return

            idcel_str = idcel_item.text()
            if not idcel_str.isdigit():
                QMessageBox.warning(self, "Error", "idcelular no es válido.")
                return

            idcel = int(idcel_str)
            resultado = delete_number.eliminar_numero_confianza(idcel)
            QMessageBox.information(self, "Eliminar Número", resultado)
            self.buscar_dni()
        elif accion == "Editar":
            QMessageBox.information(self, "Editar", "Función editar en desarrollo...")

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
