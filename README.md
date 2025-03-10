# 📲 ABM Números de Confianza - INSSSEP Chatbot  

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green?style=for-the-badge&logo=qt)
![SQL Server](https://img.shields.io/badge/Database-SQL%20Server-red?style=for-the-badge&logo=microsoftsqlserver)
![Windows](https://img.shields.io/badge/OS-Windows-lightgrey?style=for-the-badge&logo=windows)
![Status](https://img.shields.io/badge/Estado-En%20Desarrollo-orange?style=for-the-badge)

📢 **Sistema de Gestión de Números de Confianza para el Chatbot del INSSSEP**  
Este proyecto permite la **búsqueda, visualización, edición y eliminación** de números de confianza asociados a beneficiarios. Su objetivo principal es facilitar el acceso a **recibos de sueldo digitales** a través del chatbot de INSSSEP.  

---

## 🚀 **Características del Proyecto**
✔ **Búsqueda por DNI**: Obtención de datos de beneficiarios activos.  
✔ **Visualización de números de confianza** en una tabla organizada.  
✔ **Carga de nuevos números** con detalles como código de país, área, referencia y preferencias de notificación.  
✔ **Eliminación de números de confianza con confirmación previa.**  
✔ **Generación de comprobantes en PDF** con formato horizontal y datos estructurados.  
✔ **Interfaz moderna y responsiva**, con iconos y estilos optimizados.  
✔ **Integración con el chatbot del INSSSEP** para gestionar accesos a recibos digitales. 

---

## 📷 **Capturas**

### 🖥️ **Interfaz del Programa**
![Captura de la Aplicación]
[![imagen-2025-03-10-122950068.png](https://i.postimg.cc/QMXvwtyy/imagen-2025-03-10-122950068.png)](https://postimg.cc/fVrH0wZc)

### 🤖 **Opción en el Chatbot**
![Chatbot INSSSEP]
[![b5d47fc7-4305-4e7e-af7f-9377540abd0a.jpg](https://i.postimg.cc/6qdDFvtF/b5d47fc7-4305-4e7e-af7f-9377540abd0a.jpg)](https://postimg.cc/zHGtg3Lk)

### 📄 **Generación de Comprobante PDF**
![Comprobante PDF]
[![imagen-2025-03-10-123817150.png](https://i.postimg.cc/43qqd53r/imagen-2025-03-10-123817150.png)](https://postimg.cc/WDmXY0gn)

## 🔧 **Tecnologías Utilizadas**
- ![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python) **Python 3.12**
- ![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green?style=flat-square&logo=qt) **PyQt6** (Interfaz gráfica)
- ![SQL Server](https://img.shields.io/badge/SQL%20Server-Database-red?style=flat-square&logo=microsoftsqlserver) **Microsoft SQL Server**  
- **Procedimientos Almacenados SQL**
- **QSS (Estilos personalizados para PyQt6)**

---

## 📦 **Instalación y Uso**
### 1️⃣ **Clonar el repositorio**
```sh
git clone https://github.com/tu_usuario/abm_numeros_confianza.git
cd abm_numeros_confianza
```

###  2️⃣ **Crear y activar un entorno virtual**

```sh
python -m venv venv
```

###  3️⃣ **Instalar dependencias**

```sh
pip install -r requirements.txt

```
###4️⃣ **Ejecutar la aplicación**
```sh
python main.py

```

## 📂 Estructura del Proyecto
```sh
📂 abm_numeros_confianza/
│
├── 📂 assets/                 # Archivos de recursos (íconos, imágenes, estilos)
│   ├── bg.png                 # Imagen de fondo de la aplicación
│   ├── phone.png              # Ícono principal de la aplicación
│   ├── add1.png               # Ícono para agregar números
│   ├── delete1.png            # Ícono para eliminar números
│   ├── print.png              # Ícono para generar comprobantes PDF
│
├── 📂 Modules/                # Módulos principales del proyecto
│   ├── __init__.py            # Archivo de inicialización del paquete
│   ├── conexion_db.py         # Módulo para la conexión con SQL Server
│   ├── add_number.py          # Módulo para insertar nuevos números de confianza
│   ├── delete_number.py       # Módulo para eliminar números de confianza
│   ├── generate_pdf.py        # Módulo para la generación de comprobantes PDF
│   ├── styles.py              # Archivo de estilos (QSS) para la interfaz
│
├── 📂 UI/                     # Interfaz gráfica
│   ├── main_window.py         # Ventana principal del programa
│
├── 📂 output/                 # Carpeta para almacenar los PDFs generados
│   ├── comprobante_numeros.pdf # Último comprobante generado
│
├── .gitignore                 # Archivo para ignorar archivos innecesarios en Git
├── README.md                  # Documentación del proyecto
├── requirements.txt           # Dependencias del proyecto
├── main.py                    # Archivo principal para ejecutar la aplicación
│
└── venv/                      # Entorno virtual de Python (no incluido en Git)

```

## 🔗 **Conexión con la Base de Datos**

El sistema se conecta a Microsoft SQL Server con autenticación de Windows, accediendo a las bases:

Gestion (Servidor: SQL01) → Procedimientos almacenados.
DSP (Servidor: SQL01) → Datos de beneficiarios.

## 🚧 **Funcionalidades en Desarrollo**
🔜 Historial de modificaciones para control de cambios. (Auditoría)
🔜 Más opciones de integración con el chatbot de INSSSEP.

## 📄 Licencia
Este proyecto es de uso interno para INSSSEP y no está disponible para distribución pública.

