STYLE_MAIN_WINDOW = """
    /* Fondo general de la ventana */
    QWidget {
        background-color: #F6F6F6;
        font-family: Arial, sans-serif;
        font-size: 14px;
    }

    /* "Ingrese DNI" en color negro */
    QLabel#labelDni {
        background-color: transparent;
        color: black;  /* 🔹 Fuente en negro */
        font-weight: bold;
    }

    /* "Agregar Nuevo Número", "Principal" y "Notificación" en color blanco */
    QLabel#labelAgregar,
    QLabel#labelPrincipal,
    QLabel#labelNotificacion {
        background-color: transparent;
        color: white;  /* 🔹 Fuente en blanco */
        font-weight: bold;  /* 🔹 Negrita */
    }

    /* 
     * Labels transparentes para que no muestren fondo blanco, 
     * útil cuando tienes imagen de fondo en la ventana. 
     * Si quieres que TODOS los QLabel sean transparentes, 
     * usa "QLabel { background-color: transparent; }".
    */
    QLabel#labelDni,
    QLabel#labelAgregar,
    QLabel#labelPrincipal,
    QLabel#labelNotificacion {
        background-color: transparent;
    }
    
    /* Campos de texto */
    QLineEdit {
        border: 1px solid #AAAAAA;
        padding: 6px;
        border-radius: 4px;
        background-color: #FFFFFF;
    }
    QLineEdit:focus {
        border: 1px solid #0078D7; /* Resalta el borde al hacer focus */
        background-color: #FAFAFA;
    }

    /* Botones normales */
    QPushButton {
        background-color: #0078D7;
        color: white;
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

    /* Botones tipo ToolButton (íconos de Editar, Eliminar, Agregar, etc.) */
    QToolButton {
        background-color: transparent;
        border: none;
        margin: 0px 3px;
    }
    QToolButton:hover {
        background-color: #E0E0E0;
        border-radius: 4px;
    }

    /* ComboBox */
    QComboBox {
        border: 1px solid #AAAAAA;
        border-radius: 4px;
        padding: 4px;
        background-color: #FFFFFF;
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

    /* Tabla */
    QTableWidget {
        background-color: #FFFFFF;
        gridline-color: #DDDDDD;
        selection-background-color: #B5D5FF; /* Color al seleccionar una fila */
        selection-color: #000000;
    }

    /* Encabezados de la tabla */
    QHeaderView::section {
        background-color: #EAEAEA;
        padding: 4px;
        border: 1px solid #CCCCCC;
        font-weight: bold;
    }

    /* ===== ScrollBars redondeados y modernos ===== */
    /* ScrollBar vertical */
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

    /* ScrollBar horizontal */
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
