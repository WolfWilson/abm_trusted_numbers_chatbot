# Contexto del Proyecto: Migración a Web App (Django)

## 1. Descripción General
El objetivo es migrar una aplicación de escritorio (Python + PyQt6) a una aplicación web ligera utilizando **Django**. El sistema permite la gestión (ABM) de "Números de Confianza" para el Chatbot del INSSSEP, permitiendo a los operadores buscar beneficiarios por DNI y gestionar sus números de teléfono autorizados para recibir recibos de sueldo digitales.

---

## 2. Infraestructura de Datos

### Servidor y Base de Datos
- **Motor:** Microsoft SQL Server.
- **Servidor:** `SQL01`.
- **Base de Datos Principal:** `Gestion`.
- **Autenticación:** Actualmente usa `Trusted_Connection=yes` (Autenticación de Windows).
  - *Nota para Django:* Se requerirá configurar `django-mssql-backend` o `mssql-django` y definir si se usará un usuario SQL específico o Passthrough de autenticación de Windows.

### Procedimientos Almacenados (SPs)
La lógica de negocio reside casi en su totalidad en Stored Procedures dentro de la BD `Gestion`. La aplicación web no debe realizar queries directas (`SELECT/INSERT`) a las tablas, sino invocar estos SPs.

#### A. Búsqueda y Lectura
*   **SP:** `Gestion.dbo.Will_obtener_datos_chatbot_cred_test`
*   **Parámetro:** `@Nro_doc` (Entero/String - DNI del beneficiario).
*   **Retorno:** Datos del beneficiario y lista de números asociados.
*   **Uso:** Pantalla principal, al ingresar el DNI y dar "Buscar".

#### B. Altas (Crear)
*   **SP:** `Gestion.dbo.Will_agregar_numero_confianza_test`
*   **Parámetros esperados:** DNI, Código País, Código Área, Número, Referencia (ej: "Celular de Juan"), ¿Es Whatsapp? (Booleano/Bit).
*   **Uso:** Formulario modal o página de "Agregar Número".

#### C. Bajas (Eliminar)
*   **SP:** `Gestion.dbo.Will_eliminar_numero_confianza_test`
*   **Parámetros esperados:** ID del registro o combinación de DNI + Número.
*   **Uso:** Botón de eliminar en la tabla de resultados.

#### D. Modificaciones (Editar)
*   **SP:** `Gestion.dbo.Will_editar_numero_confianza_test`
*   **Uso:** Modificar referencia o corregir un número mal cargado.

#### E. Seguridad (Permisos)
*   **SP:** `Gestion.dbo.Tiene_permiso`
*   **Parámetro:** `grupo_nt` (Nombre del grupo de red/usuario).
*   **Lógica:** Devuelve `1` si tiene permiso, `0` si no.
*   **Retorno:** Columna `puede`.

---

## 3. Flujo de la Aplicación (User Journey)

1.  **Login / Verificación de Acceso:**
    *   Al entrar a la web, el sistema debe validar si el usuario tiene permisos.
    *   *Actual:* Verifica el grupo de Windows local contra el SP `Tiene_permiso`.
    *   *Web:* Se deberá decidir si se usa el sistema de usuarios de Django (`auth_user`) o si se valida contra el SP al momento del login.

2.  **Búsqueda (Home):**
    *   Input único para ingresar DNI.
    *   Botón "Buscar".

3.  **Resultados y Gestión:**
    *   Si el DNI existe: Muestra nombre del beneficiario y una tabla con los números cargados.
    *   **Acciones en tabla:** Botones para "Editar" y "Eliminar" por cada fila.
    *   **Acción Global:** Botón "Agregar Nuevo Número".

4.  **Generación de Comprobante:**
    *   Botón "Imprimir / Generar PDF".
    *   Debe generar un PDF (Server-side con librerías como `WeasyPrint` o `ReportLab`) con el listado de números activos para que el beneficiario firme.

---

## 4. Requerimientos Técnicos para Django

### Dependencias Clave Sugeridas
*   `django`
*   `mssql-django` (Driver recomendado para SQL Server).
*   `pyodbc` (Driver ODBC subyacente).
*   `weasyprint` o `xhtml2pdf` (Para generar el comprobante PDF desde HTML).

### Estructura de Modelos
Dado que es una base de datos legacy/externa basada en SPs, **no es necesario crear modelos de Django (`models.py`) gestionados (managed=True)** para las tablas de negocio.
*   Se pueden usar modelos `managed=False` si se necesita inspeccionar tablas.
*   Lo más eficiente es crear una capa de servicio (`services.py` o `repositories.py`) que ejecute los `cursor.execute("EXEC ...")` directamente.

### Frontend
*   Plantillas HTML simples (Django Templates).
*   Bootstrap o TailwindCSS para replicar la interfaz limpia actual.
*   Uso de Modales para "Agregar/Editar" para mantener la experiencia de usuario (UX) fluida.
