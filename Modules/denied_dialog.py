import sys
import os
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QSize

def show_access_denied_dialog():
    """
    Muestra una ventana QDialog con denied2.gif (animado) y un mensaje original en negrita.
    Al presionar 'OK', cierra la aplicación con sys.exit(0).
    """
    dialog = QDialog()
    dialog.setWindowTitle("Acceso Denegado")
    dialog.setFixedSize(400, 300)

    # Para quitar minimizar / maximizar / help:
    dialog.setWindowFlags(
        Qt.WindowType.Dialog
        | Qt.WindowType.WindowTitleHint
        | Qt.WindowType.CustomizeWindowHint
    )

    layout = QVBoxLayout(dialog)

    # 1) Imagen centrada (GIF animado con QMovie)
    ruta_gif = os.path.join(os.path.dirname(__file__), "..", "assets", "denied2.gif")
    label_imagen = QLabel()
    if os.path.exists(ruta_gif):
        movie = QMovie(ruta_gif)
        movie.setScaledSize(QSize(200, 200))  # Escalar GIF si es necesario
        label_imagen.setMovie(movie)
        movie.start()  # Inicia la animación
    else:
        label_imagen.setText("No se encontró 'denied2.gif' en assets/")
    label_imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(label_imagen)

    # 2) Mensaje en negrita
    mensaje = (
        "<b>¡Acceso denegado! Pero mira el lado positivo: menos trabajo por ahora. :)</b><br><br>"
        "<b>Si crees que esto es un error, contacta al Área de Sistemas.</b>"
    )
    label_texto = QLabel(mensaje)
    label_texto.setWordWrap(True)
    label_texto.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label_texto.setTextFormat(Qt.TextFormat.RichText)  # Habilitar HTML
    layout.addWidget(label_texto)

    # 3) Botón OK
    btn_ok = QPushButton("OK")
    btn_ok.clicked.connect(lambda: close_app(dialog))
    layout.addWidget(btn_ok, alignment=Qt.AlignmentFlag.AlignCenter)

    dialog.exec()

def close_app(dialog: QDialog):
    """
    Cierra el diálogo y sale de la aplicación.
    """
    dialog.accept()
    sys.exit(0)
