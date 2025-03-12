#Modules/conexion_db.py
import pyodbc

def get_connection():
    drivers = [
        '{SQL Server Native Client 10.0}',  #  Driver específico para SQL Server 2012 (forzado)
        '{SQL Server Native Client 11.0}',  # Alternativa si falla
        '{ODBC Driver 13 for SQL Server}',  # Opción adicional
        '{ODBC Driver 17 for SQL Server}'   # Última versión, solo si fallan las anteriores
    ]
    server = 'SQL01'
 #   server = 'PC-2193' # SERVER PARA PRUEBAS
    database = 'Gestion'

    for driver in drivers:
        try:
            print(f"Probando conexión con {driver}...")
            conn = pyodbc.connect(
                f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
            )
            print("Conexión exitosa.")
            return conn
        except pyodbc.Error as e:
            print(f"Error al conectar con {driver}: {e}")

    raise Exception("No se pudo conectar a la base de datos con ningún driver.")

def buscar_por_dni(dni):
    """
    Ejecuta el procedimiento almacenado Will_obtener_datos_chatbot_cred para obtener datos del DNI.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = "EXEC Gestion.dbo.Will_obtener_datos_chatbot_cred_test @Nro_doc = ?"
        cursor.execute(query, (dni,))
        columnas = [column[0] for column in cursor.description]  # Obtener nombres de columnas
        resultados = cursor.fetchall()

        if resultados:
            return [dict(zip(columnas, row)) for row in resultados]
        else:
            return []
    except Exception as e:
        print(f"Error ejecutando la consulta: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def verificar_permiso(grupo_nt):
    """
    Consulta el procedimiento almacenado 'Tiene_permiso' en la BD.
    Devuelve True si el usuario tiene acceso, False si no.
    """
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=PC-2193;"
            "DATABASE=Gestion;"
            "Trusted_Connection=yes;"
        )
        cursor = conn.cursor()

        cursor.execute("EXEC Tiene_permiso ?", grupo_nt)
        resultado = cursor.fetchone()

        conn.close()

        return resultado and resultado[0] == 1  # True si tiene permiso

    except Exception as e:
        print(f"❌ Error en la validación de permisos: {e}")
        return False  # En caso de error, denegar acceso



