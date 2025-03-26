STYLE_MAIN_WINDOW = """
    QWidget {
        color: #f7edf8;
        background-color: transparent;
        font-family: Arial, sans-serif;
        font-size: 14px;
        
    }

    QLabel#labelDni {
        background-color: transparent;
        color: #000000;  /* Texto negro (visible en fondo claro) */
        font-weight: bold;
    }

    QLabel#labelAgregar,
    QLabel#labelPrincipal,
    QLabel#labelNotificacion {
        background-color: transparent;
        color: #FFFFFF;  /* Texto blanco para contraste */
        font-weight: bold;
    }

    QLineEdit {
        border: 1px solid #AAAAAA;
        padding: 6px;
        border-radius: 4px;
        background-color: #FFFFFF;
        color: #000000;  /* Texto oscuro en cajas de entrada */
    }
    QLineEdit:focus {
        border: 1px solid #0078D7;
        background-color: #FAFAFA;
        color: #000000;
    }

    QPushButton {
        background-color: #0078D7;
        color: #FFFFFF;
        border-radius: 4px;
        padding: 6px 10px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #005A9E;
    }
    QPushButton:pressed {
        background-color: #003E73;
    }

    QToolButton {
        background-color: transparent;
        border: none;
        margin: 0px 3px;
    }
    QToolButton:hover {
        background-color: #E0E0E0;
        border-radius: 4px;
    }

    QComboBox {
        border: 1px solid #AAAAAA;
        border-radius: 4px;
        padding: 4px;
        background-color: #FFFFFF;
        color: #000000;
    }
    QComboBox:focus {
        border: 1px solid #0078D7;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left: 0px solid darkgray;
    }

    QTableWidget {
        background-color: #FFFFFF;
        color: #000000;
        gridline-color: #DDDDDD;
        selection-background-color: #B5D5FF;
        selection-color: #000000;
    }

    QHeaderView::section {
        background-color: #EAEAEA;
        color: #000000;
        padding: 4px;
        border: 1px solid #CCCCCC;
        font-weight: bold;
    }

    QScrollBar:vertical {
        border: none;
        background-color: #E0E0E0;
        width: 10px;
        margin: 0px 0px 0px 0px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical {
        background-color: #AAAAAA;
        min-height: 30px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #999999;
    }
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {
        background: none;
        border: none;
        height: 0px;
    }

    QScrollBar:horizontal {
        border: none;
        background-color: #E0E0E0;
        height: 10px;
        margin: 0px 0px 0px 0px;
        border-radius: 5px;
    }
    QScrollBar::handle:horizontal {
        background-color: #AAAAAA;
        min-width: 30px;
        border-radius: 5px;
    }
    QScrollBar::handle:horizontal:hover {
        background-color: #999999;
    }
    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {
        background: none;
        border: none;
        width: 0px;
    }
"""
