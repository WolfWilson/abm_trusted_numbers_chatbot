# Modules/conexion_db.py

import pyodbc

def get_connection(server="SQL01", database="Gestion"):
    """
    Intenta conectarse a SQL Server permitiendo seleccionar servidor y base de datos.
    Por defecto, usa server='SQL01' y database='Gestion'.
    """
    drivers = [
        '{SQL Server Native Client 10.0}',  # Forzado para SQL Server 2012
        '{SQL Server Native Client 11.0}',  # Alternativa si falla
        '{ODBC Driver 13 for SQL Server}',  # Opción adicional
        '{ODBC Driver 17 for SQL Server}'   # Última versión
    ]

    for driver in drivers:
        try:
            print(f"🔄 Probando conexión con {driver} en {server}\\{database}...")
            conn = pyodbc.connect(
                f'DRIVER={driver};'
                f'SERVER={server};'
                f'DATABASE={database};'
                'Trusted_Connection=yes;'
            )
            print(f"✅ Conexión exitosa a {server}\\{database} con {driver}.")
            return conn
        except pyodbc.Error as e:
            print(f"❌ Error con {driver} en {server}\\{database}: {e}")

    raise Exception(f"⚠ No se pudo conectar a la base de datos {database} en {server} con ningún driver.")

def ejecutar_procedimiento(server, database, query, parametros=()):
    """
    Ejecuta un procedimiento almacenado en el servidor y base de datos especificados.
    Devuelve los resultados como lista de diccionarios, o lista vacía si no hay filas.
    """
    conn = get_connection(server, database)
    cursor = conn.cursor()

    try:
        cursor.execute(query, parametros)
        columnas = [col[0] for col in cursor.description] if cursor.description else []
        filas = cursor.fetchall()

        return [dict(zip(columnas, row)) for row in filas] if filas else []
    except Exception as e:
        print(f"⚠ Error ejecutando la consulta en {server}\\{database}: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def buscar_por_dni(dni):
    """
    Obtiene datos del beneficiario según el DNI desde la base 'Gestion' en el servidor 'SQL01'.
    """
    query = "EXEC Gestion.dbo.Will_obtener_datos_chatbot_cred_test @Nro_doc = ?"
    return ejecutar_procedimiento("SQL01", "Gestion", query, (dni,))

def verificar_permiso(grupo_nt):
    """
    Llama al procedimiento 'Tiene_permiso' en el servidor=SQL01, base=Gestion,
    para verificar si el usuario tiene acceso.
    """
    query = "EXEC Tiene_permiso ?"
    resultado = ejecutar_procedimiento("SQL01", "Gestion", query, (grupo_nt,))
    
    return resultado and resultado[0].get("puede", 0) == 1
