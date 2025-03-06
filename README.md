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
✔ **Edición y eliminación de números de confianza** *(Próximamente)*.  
✔ **Interfaz moderna y responsiva**, con iconos y estilos optimizados.  
✔ **Integración con el chatbot del INSSSEP** para gestionar accesos a recibos digitales.  

---

## 📷 **Capturas**

### 🖥️ **Interfaz del Programa**
![Captura de la Aplicación](ruta/a/captura1.png)

### 🤖 **Opción en el Chatbot**
![Chatbot INSSSEP](ruta/a/captura2.png)


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

## 🔗 **Conexión con la Base de Datos**

El sistema se conecta a Microsoft SQL Server con autenticación de Windows, accediendo a las bases:

Gestion (Servidor: SQL01) → Procedimientos almacenados.
DSP (Servidor: SQL01) → Datos de beneficiarios.

## 🚧 Próximas Funcionalidades
🔜 Edición de números de confianza para actualizar datos.
🔜 Eliminación de números con confirmación previa.
🔜 Historial de modificaciones para control de cambios.
🔜 Más opciones de integración con el chatbot de INSSSEP.

📄 Licencia
Este proyecto es de uso interno para INSSSEP y no está disponible para distribución pública.

