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
from Modules import edit_number  # <-- Importamos el nuevo módulo para editar

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
        # Variables para modo edición
        self.edit_mode = False
        self.edit_idcel = None

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

        # Dos líneas máximo
        self.table.setWordWrap(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Anchos fijos
        self.table.setColumnWidth(1, 160)  # Nombre
        self.table.setColumnWidth(2, 160)  # Referencia
        self.table.setColumnWidth(3, 130)  # Teléfono
        self.table.setColumnWidth(4, 80)   # Principal
        self.table.setColumnWidth(5, 100)  # Notificación
        self.table.setColumnWidth(6, 80)   # Estado
        self.table.setColumnWidth(7, 120)  # Beneficio
        self.table.setColumnWidth(8, 70)   # Editar
        self.table.setColumnWidth(9, 70)   # Eliminar

        self.table.verticalHeader().setDefaultSectionSize(40)

        layout.addWidget(self.table)

        # Sección "Agregar Nuevo Número" (o editar)
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
        self.btn_agregar.setIconSize(QSize(80, 80))
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
        self.btn_agregar.clicked.connect(self.on_agregar_o_editar)

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
        self.edit_mode = False
        self.edit_idcel = None
        self.label_agregar.setText("Agregar Nuevo Número")
        self.btn_agregar.setToolTip("Agregar nuevo número")

        dni = self.input_dni.text().strip()
        if dni.isdigit():
            resultado = buscar_por_dni(int(dni))
            self.mostrar_resultados(resultado)
        else:
            self.mostrar_resultados([])

    def mostrar_resultados(self, resultados):
        self.table.setRowCount(len(resultados))
        self.current_cuil = None

        for row, data in enumerate(resultados):
            if row == 0:
                self.current_cuil = data.get("CUIL", None)

            idcel = data.get("idcelular", "")
            self.table.setItem(row, 0, QTableWidgetItem(str(idcel)))

            nombre_text = str(data.get("Nombre", ""))
            self.table.setItem(row, 1, QTableWidgetItem(nombre_text))

            referencia_text = str(data.get("referencia", ""))
            self.table.setItem(row, 2, QTableWidgetItem(referencia_text))

            telefono_text = str(data.get("telefono", ""))
            self.table.setItem(row, 3, QTableWidgetItem(telefono_text))

            principal_text = "Sí" if data.get("principal", 0) else "No"
            self.table.setItem(row, 4, QTableWidgetItem(principal_text))

            notif_text = "Sí" if data.get("notificacion", 0) else "No"
            self.table.setItem(row, 5, QTableWidgetItem(notif_text))

            activo_val = data.get("Activo", 1)
            activo_text = "Activo" if activo_val == 0 else "Inactivo"
            self.table.setItem(row, 6, QTableWidgetItem(activo_text))

            benef_text = str(data.get("Tipo_Benef", ""))
            self.table.setItem(row, 7, QTableWidgetItem(benef_text))

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

    def on_agregar_o_editar(self):
        """
        Si estamos en modo edicion (self.edit_mode=True), se edita
        caso contrario, se agrega.
        """
        if not self.current_cuil and not self.edit_mode:
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

        if not self.edit_mode:
            # Modo Agregar
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

            # Insertar
            resultado = add_number.agregar_numero_confianza(
                cuil=self.current_cuil,
                pais=pais,
                area=area,
                abonado=abonado,
                referencia=referencia,
                principal=principal,
                notificacion=notificacion
            )
            QMessageBox.information(self, "Agregar Número", resultado)
        else:
            # Modo Editar
            if not self.edit_idcel:
                QMessageBox.warning(self, "Error", "No se encontró el ID del número a editar.")
                return

            confirm_msg = f"¿Está seguro que desea editar el número:\n" \
                          f"{pais} {area} {abonado}\n" \
                          f"Referencia: {referencia}"
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Confirmar Edición")
            msg_box.setText(confirm_msg)
            msg_box.setIcon(QMessageBox.Icon.Question)
            btn_si = msg_box.addButton("Sí", QMessageBox.ButtonRole.YesRole)
            btn_no = msg_box.addButton("No", QMessageBox.ButtonRole.NoRole)
            msg_box.exec()

            if msg_box.clickedButton() == btn_no:
                return

            # Editar
            from Modules import edit_number
            resultado = edit_number.editar_numero_confianza(
                idcelular=self.edit_idcel,
                pais=pais,
                area=area,
                abonado=abonado,
                referencia=referencia,
                principal=principal,
                notificacion=notificacion
            )
            QMessageBox.information(self, "Editar Número", resultado)

            # Restaurar modo
            self.edit_mode = False
            self.edit_idcel = None
            self.label_agregar.setText("Agregar Nuevo Número")
            self.btn_agregar.setToolTip("Agregar nuevo número")

        # Limpiar
        self.input_pais.clear()
        self.input_area.clear()
        self.input_numero.clear()
        self.input_referencia.clear()
        self.combo_principal.setCurrentIndex(0)
        self.combo_notificacion.setCurrentIndex(0)

        self.buscar_dni()

    def confirmar_accion(self, accion, row):
        """
        Para "Editar", cargamos los datos en el formulario y pasamos a modo edicion.
        Para "Eliminar", llamamos a delete.
        """
        if accion == "Eliminar":
            mensaje = f"¿Está seguro que desea eliminar este número?"
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(f"{accion} Número")
            msg_box.setText(mensaje)
            msg_box.setIcon(QMessageBox.Icon.Question)
            btn_si = msg_box.addButton("Sí", QMessageBox.ButtonRole.YesRole)
            btn_no = msg_box.addButton("No", QMessageBox.ButtonRole.NoRole)
            msg_box.exec()

            if msg_box.clickedButton() == btn_no:
                return

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
            # 1) Tomar idcelular
            idcel_item = self.table.item(row, 0)
            if not idcel_item:
                QMessageBox.warning(self, "Error", "No se encontró idcelular.")
                return

            idcel_str = idcel_item.text()
            if not idcel_str.isdigit():
                QMessageBox.warning(self, "Error", "idcelular inválido.")
                return

            self.edit_idcel = int(idcel_str)

            # 2) Cargar datos de la fila en el formulario
            nombre_item = self.table.item(row, 1)
            referencia_item = self.table.item(row, 2)
            tel_item = self.table.item(row, 3)
            principal_item = self.table.item(row, 4)
            notif_item = self.table.item(row, 5)

            # Asumimos que la tabla no guarda por separado el pais, area y abonado, 
            # sino "Teléfono" completo. Tocaría parsear "54 362 4219426" si quisieras. 
            # En este ejemplo, supondremos que el usuario rellena manualmente o 
            # que la DB devolvía pais, area, abonado separadamente en celdas. 

            # Si tu SP realmente devuelve 'pais','area','abonado' en columns, 
            # asigna: 
            # self.input_pais.setText(self.table.item(row, X).text()) 
            # etc.

            # De momento, supondremos que "Teléfono" no se parsea.

            self.input_referencia.setText(referencia_item.text())

            # Principal
            if principal_item.text() == "Sí":
                self.combo_principal.setCurrentText("Sí")
            else:
                self.combo_principal.setCurrentText("No")

            # Notificacion
            if notif_item.text() == "Sí":
                self.combo_notificacion.setCurrentText("Sí")
            else:
                self.combo_notificacion.setCurrentText("No")

            # 3) Modo edicion activado
            self.edit_mode = True
            self.label_agregar.setText("Editar Número")
            self.btn_agregar.setToolTip("Guardar cambios del número")

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
