# Modules/add_number.py

import pyodbc
from Modules.conexion_db import get_connection

def agregar_numero_confianza(cuil, pais, area, abonado, referencia, principal, notificacion):
    """
    Llama al procedimiento 'Will_agregar_numero_confianza_test'
    para insertar un nuevo número de confianza.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            EXEC Will_agregar_numero_confianza_test 
                @Cuil=?,
                @Pais=?,
                @Area=?,
                @Abonado=?,
                @Referencia=?,
                @Principal=?,
                @Notificacion=?
        """, (cuil, pais, area, abonado, referencia, principal, notificacion))
        conn.commit()

        # No se está leyendo la salida PRINT del SP, 
        # pero podríamos capturar con cursor.messages si quisiéramos.
        return "Número agregado correctamente."
    except Exception as e:
        return f"Error al agregar número: {e}"
    finally:
        cursor.close()
        conn.close()
