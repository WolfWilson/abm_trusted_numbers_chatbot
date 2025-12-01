
import pyodbc

def get_connection(server="SQL01", database="Gestion"):
    """
    Intenta conectarse a SQL Server permitiendo seleccionar servidor y base de datos.
    Compatible con drivers desde SQL Server 2008 en adelante.
    """
    drivers = [
        '{SQL Server Native Client 11.0}',
        '{SQL Server Native Client 10.0}',
        '{SQL Server Native Client 2008}',
        '{SQL Server}',
        '{ODBC Driver 17 for SQL Server}',
        '{ODBC Driver 13 for SQL Server}',
        '{ODBC Driver 11 for SQL Server}'
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
    Ejecuta un procedimiento almacenado y devuelve resultados como lista de dicts.
    Si hay errores, devuelve un dict con clave 'error'.
    """
    try:
        conn = get_connection(server, database)
        cursor = conn.cursor()

        cursor.execute(query, parametros)

        if cursor.description:
            columnas = [col[0] for col in cursor.description]
            filas = cursor.fetchall()
            return [dict(zip(columnas, row)) for row in filas] if filas else []
        else:
            return []

    except pyodbc.ProgrammingError as e:
        return {"error": f"Error de sintaxis o SP malformado: {e}"}
    except pyodbc.OperationalError as e:
        return {"error": f"Error operacional (servidor inaccesible, timeout, etc): {e}"}
    except pyodbc.Error as e:
        return {"error": f"Error ODBC o de conexión general: {e}"}
    except Exception as e:
        return {"error": f"Error inesperado: {e}"}
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def buscar_por_dni(dni):
    """
    Llama al procedimiento en Gestion y devuelve datos o mensaje de error.
    """
    query = "EXEC Gestion.dbo.Will_obtener_datos_chatbot_cred_test @Nro_doc = ?"
    resultado = ejecutar_procedimiento("SQL01", "Gestion", query, (dni,))
    
    if isinstance(resultado, dict) and "error" in resultado:
        print(f"⚠ Error interno al buscar DNI {dni}: {resultado['error']}")
        return [f"ERROR: {resultado['error']}"]

    return resultado


def verificar_permiso(grupo_nt):
    """
    Verifica si el grupo tiene acceso según el SP Tiene_permiso.
    """
    query = "EXEC Tiene_permiso ?"
    
    resultado = ejecutar_procedimiento("SQL01", "Gestion", query, (grupo_nt,))
    
    if isinstance(resultado, dict) and "error" in resultado:
        print(f"⚠ Error al verificar permiso para {grupo_nt}: {resultado['error']}")
        return False

    return resultado and resultado[0].get("puede", 0) == 1
