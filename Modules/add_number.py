from Modules.conexion_db import get_connection

def agregar_numero_confianza(cuil, pais, area, abonado, referencia, principal, notificacion):
    # Conecta a servidor=Principal, base=Credenciales
    conn = get_connection(server="Principal", database="Credenciales")
    cursor = conn.cursor()
    try:
        # Ojo: Si el SP está en schema dbo, la llamada es:
        cursor.execute("""
            EXEC dbo.Will_agregar_numero_confianza_test
                @Cuil=?,
                @Pais=?,
                @Area=?,
                @Abonado=?,
                @Referencia=?,
                @Principal=?,
                @Notificacion=?
        """, (cuil, pais, area, abonado, referencia, principal, notificacion))
        conn.commit()
        return "✅ Número agregado correctamente."
    except Exception as e:
        return f"❌ Error al agregar número: {e}"
    finally:
        cursor.close()
        conn.close()
