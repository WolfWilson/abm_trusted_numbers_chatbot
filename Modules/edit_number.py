# Modules/edit_number.py

import pyodbc
from Modules.conexion_db import get_connection

def editar_numero_confianza(idcelular, pais, area, abonado, referencia, principal, notificacion):
    """
    Llama al procedimiento 'Will_editar_numero_confianza_test'
    para actualizar un número de confianza.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            EXEC Will_editar_numero_confianza_test 
                @idcelular=?,
                @Pais=?,
                @Area=?,
                @Abonado=?,
                @Referencia=?,
                @Principal=?,
                @Notificacion=?
        """, (idcelular, pais, area, abonado, referencia, principal, notificacion))
        conn.commit()

        return "Número editado correctamente."
    except Exception as e:
        return f"Error al editar número: {e}"
    finally:
        cursor.close()
        conn.close()
