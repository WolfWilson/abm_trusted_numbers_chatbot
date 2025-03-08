# Modules/delete_number.py

import pyodbc
from Modules.conexion_db import get_connection

def eliminar_numero_confianza(idcelular):
    """
    Llama al procedimiento 'Will_eliminar_numero_confianza_test'
    para eliminar un número de confianza por idcelular.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            EXEC Will_eliminar_numero_confianza_test
                @idcelular=?
        """, (idcelular,))
        conn.commit()
        return "Número eliminado correctamente."
    except Exception as e:
        return f"Error al eliminar número: {e}"
    finally:
        cursor.close()
        conn.close()
