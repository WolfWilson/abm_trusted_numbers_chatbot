import os
import sys
import subprocess
import platform
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QComboBox, QToolButton, QMessageBox, QHeaderView
)
from PyQt6.QtGui import QGuiApplication, QIcon, QPixmap, QPalette, QBrush
from PyQt6.QtCore import QSize, Qt

# Módulos del proyecto
from Modules.conexion_db import buscar_por_dni
from Modules.styles import STYLE_MAIN_WINDOW
from Modules import add_number
from Modules import delete_number

# Para generar el PDF (ReportLab).
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# ====== Import reportlab (platypus) para tablas con multiline ======
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from PyQt6.QtWidgets import QApplication, QMessageBox
import sys
import getpass
from Modules.conexion_db import verificar_permiso

# Funciones auxiliares
def cargar_icono(nombre):
    ruta_base = os.path.abspath(os.path.dirname(__file__))
    ruta_icono = os.path.join(ruta_base, "..", "assets", nombre)
    return QIcon(ruta_icono)

    
def abrir_pdf(pdf_path):
    """
    Abre el archivo PDF con el visor predeterminado del sistema.
    """
    if platform.system() == 'Windows':
        os.startfile(pdf_path)  # type: ignore
    elif platform.system() == 'Darwin':  # macOS
        subprocess.run(['open', pdf_path])
    else:  # Linux / otros
        subprocess.run(['xdg-open', pdf_path])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ABM Números de Confianza")
        self.setFixedSize(1020, 500)
        self.centrar_ventana()

        self.setWindowIcon(cargar_icono("phone.png"))
        self.setStyleSheet(STYLE_MAIN_WINDOW)
        self.aplicar_fondo_ventana()

        self.current_cuil = None

        layout = QVBoxLayout()

        # ========== Sección Búsqueda ==========
        self.label_dni = QLabel("Ingrese DNI:")
        self.label_dni.setObjectName("labelDni")  # Para transparencia (styles.py)
        self.input_dni = QLineEdit()
        self.btn_buscar = QPushButton("Buscar")

        layout.addWidget(self.label_dni)
        layout.addWidget(self.input_dni)
        layout.addWidget(self.btn_buscar)

        # ========== Tabla ==========
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "idcelular (oculto)", "Nombre", "Referencia", "Teléfono",
            "Principal", "Notificación", "Estado", "Beneficio", "Eliminar"
        ])
        self.table.setColumnHidden(0, True)  # Ocultamos col idcel

        self.table.setWordWrap(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        # Ajustar anchos
        self.table.setColumnWidth(1, 180)  # Nombre
        self.table.setColumnWidth(2, 200)  # Referencia
        self.table.setColumnWidth(3, 130)  # Teléfono
        self.table.setColumnWidth(4, 80)   # Principal
        self.table.setColumnWidth(5, 100)  # Notificación
        self.table.setColumnWidth(6, 80)   # Estado
        self.table.setColumnWidth(7, 120)  # Beneficio
        self.table.setColumnWidth(8, 70)   # Eliminar

        self.table.verticalHeader().setDefaultSectionSize(40)
        layout.addWidget(self.table)

        # ========== Sección Agregar Número ==========
        self.label_agregar = QLabel("Agregar Nuevo Número")
        self.label_agregar.setObjectName("labelAgregar")  # Para transparencia
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

        # Labels con objectName para transparencia
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
        self.btn_agregar.setIconSize(QSize(80, 80))
        self.btn_agregar.setFixedSize(80, 50)

        form_layout.addWidget(self.input_pais)
        form_layout.addWidget(self.input_area)
        form_layout.addWidget(self.input_numero)
        form_layout.addWidget(self.input_referencia)

        sub_layout = QVBoxLayout()
        sub_layout.addWidget(self.label_principal)
        sub_layout.addWidget(self.combo_principal)
        sub_layout.addWidget(self.label_notificacion)
        sub_layout.addWidget(self.combo_notificacion)
        form_layout.addLayout(sub_layout)

        # Layout vertical para el botón Add y el botón Print
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.btn_agregar)

        # Nuevo botón "Comprobante" para PDF
        self.btn_comprobante = QToolButton()
        self.btn_comprobante.setIcon(cargar_icono("print.png"))
        self.btn_comprobante.setToolTip("Generar comprobante PDF")
        self.btn_comprobante.setIconSize(QSize(60, 60))
        self.btn_comprobante.setFixedSize(80, 50)
        self.btn_comprobante.clicked.connect(self.on_generar_comprobante)
        buttons_layout.addWidget(self.btn_comprobante)

        form_layout.addLayout(buttons_layout)
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
        """
        Busca beneficiarios por DNI. Si no hay resultados, muestra una alerta.
        """
        dni = self.input_dni.text().strip()

        if not dni.isdigit():
            QMessageBox.warning(self, "Error", "El DNI ingresado no es válido. Debe contener solo números.")
            return

        resultado = buscar_por_dni(int(dni))

        if not resultado:
            # 🛑 Si no hay resultados, mostrar alerta
            QMessageBox.information(self, "Sin resultados", "No se encontraron datos para el DNI ingresado o no es JUBILADO/PENSIONADO")
            self.mostrar_resultados([])  # Limpiar tabla
            return

        self.mostrar_resultados(resultado)


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
            estado_text = "Activo" if activo_val == 0 else "Inactivo"
            self.table.setItem(row, 6, QTableWidgetItem(estado_text))

            benef_text = str(data.get("Tipo_Benef", ""))
            self.table.setItem(row, 7, QTableWidgetItem(benef_text))

            # Botón Eliminar
            btn_eliminar = QToolButton()
            btn_eliminar.setIcon(cargar_icono("delete1.png"))
            btn_eliminar.setIconSize(QSize(30, 30))
            btn_eliminar.setToolTip("Eliminar número")
            btn_eliminar.clicked.connect(lambda _, r=row: self.confirmar_eliminar(r))
            self.table.setCellWidget(row, 8, btn_eliminar)

    def confirmar_eliminar(self, row):
        mensaje = "¿Está seguro que desea eliminar este número?"
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Eliminar Número")
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
        QMessageBox.information(self, "Agregar Número", resultado)

        # Limpiar
        self.input_pais.clear()
        self.input_area.clear()
        self.input_numero.clear()
        self.input_referencia.clear()
        self.combo_principal.setCurrentIndex(0)
        self.combo_notificacion.setCurrentIndex(0)

        self.buscar_dni()

    def on_generar_comprobante(self):
        """
        Genera un PDF en hoja vertical (A4) con word-wrap real en la tabla,
        fecha y firma alineadas a la derecha, y texto principal justificado.
        """
        import os
        from datetime import datetime
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Table,
                                        TableStyle, Spacer)
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import cm
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT
        from reportlab.lib import colors

        # 1) Obtener datos de la tabla (GUI)
        row_count = self.table.rowCount()
        headers = ["Nombre", "Referencia", "Teléfono",
                "Principal", "Notificación", "Estado", "Beneficio"]
        data_rows = []

        # Creamos un estilo de celda para word-wrap
        styles = getSampleStyleSheet()
        cell_style = ParagraphStyle(
            'CellStyle',
            parent=styles['Normal'],
            fontSize=8,
            leading=10,
            alignment=TA_JUSTIFY  # Justificado en la celda
        )

        for r in range(row_count):
            nombre = self.table.item(r, 1).text() if self.table.item(r, 1) else ""
            ref    = self.table.item(r, 2).text() if self.table.item(r, 2) else ""
            tel    = self.table.item(r, 3).text() if self.table.item(r, 3) else ""
            prin   = self.table.item(r, 4).text() if self.table.item(r, 4) else ""
            notif  = self.table.item(r, 5).text() if self.table.item(r, 5) else ""
            estado = self.table.item(r, 6).text() if self.table.item(r, 6) else ""
            benef  = self.table.item(r, 7).text() if self.table.item(r, 7) else ""

            # Convertimos cada texto en un Paragraph para que se ajuste (word-wrap).
            nombre_p = Paragraph(nombre, cell_style)
            ref_p    = Paragraph(ref, cell_style)
            tel_p    = Paragraph(tel, cell_style)
            prin_p   = Paragraph(prin, cell_style)
            notif_p  = Paragraph(notif, cell_style)
            estado_p = Paragraph(estado, cell_style)
            benef_p  = Paragraph(benef, cell_style)

            data_rows.append([nombre_p, ref_p, tel_p, prin_p, notif_p, estado_p, benef_p])

        # 2) Configurar el PDF en Vertical (A4)
        # Obtener la ruta de la carpeta Descargas del usuario
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Definir el nombre y la ruta completa del PDF
        pdf_path = os.path.join(download_folder, "comprobante_numeros.pdf")
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        story = []

        # 3) Estilos para el texto general
        #    a) Fecha y Firma (alineación derecha)
        right_style = ParagraphStyle(
            'RightStyle',
            parent=styles['Normal'],
            alignment=TA_RIGHT,
            fontSize=10,
            leading=12
        )
        #    b) Texto principal (justificado)
        nota_style = ParagraphStyle(
            'NotaStyle',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            fontSize=10,
            leading=12
        )

        # 4) Fecha alineada a la derecha
        hoy = datetime.now().strftime("%d/%m/%Y")
        fecha_paragraph = Paragraph(f"Resistencia, {hoy}", right_style)
        story.append(fecha_paragraph)
        story.append(Spacer(1, 0.5*cm))

        # 5) Texto principal justificado
        texto_inicial = """
        Por medio de la presente, declaro que los números de celular que figuran a continuación,
        pertenecen a personas de mi entera confianza y autorizo a los mismos a operar
        en el CHATBOT del InSSSeP, consultando todos los datos disponibles al momento
        o los que decida el InSSSeP incorporar.<br/><br/>
        Declaro, además, que ante cualquier cambio de los datos declarados,
        informaré al InSSSeP a la brevedad.
        """
        texto_paragraph = Paragraph(texto_inicial, nota_style)
        story.append(texto_paragraph)
        story.append(Spacer(1, 0.5*cm))

        # 6) Firma a la derecha
        firma_paragraph = Paragraph(
            "<br/><br/>"  # ⬅ Agrega dos saltos de línea
            "…………………………<br/>"
            "<b>Apellido y Nombre</b><br/>"
            "<b>CUIL</b>",
            styles['Normal']
        )
        story.append(firma_paragraph)

        story.append(Spacer(1, 0.8*cm))

        # 7) Construir la tabla
        table_data = [headers] + data_rows
        # Anchos totales ~16.5 cm para no recortar.
        col_widths = [2.7*cm, 2.7*cm, 2.7*cm, 1.5*cm, 1.8*cm, 1.5*cm, 3.0*cm]

        from reportlab.platypus import Table, TableStyle
        tbl = Table(table_data, colWidths=col_widths, repeatRows=1)

        # 8) Estilo de la tabla
        tbl_style = TableStyle([
            ('WORDWRAP', (0, 0), (-1, -1), True),   # Habilitar word-wrap en celdas
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            # Encabezado
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ])
        tbl.setStyle(tbl_style)

        story.append(tbl)

        # 9) Construir PDF
        doc.build(story)

        # 10) Abrir PDF
        abrir_pdf(pdf_path)
        QMessageBox.information(self, "Comprobante", f"Se generó el comprobante:\n{pdf_path}")


    def centrar_ventana(self):
        pantalla = QGuiApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(pantalla.center())
        self.move(ventana.topLeft())


# Verifica permisos antes de abrir la aplicación
if __name__ == "__main__":
    app = QApplication([])
    from main_window import MainWindow  # Importar la ventana principal solo si tiene acceso
    window = MainWindow()
    window.show()
    app.exec()

