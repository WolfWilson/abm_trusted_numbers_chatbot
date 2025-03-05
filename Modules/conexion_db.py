import pyodbc

def get_connection():
    drivers = [
        '{ODBC Driver 17 for SQL Server}',
        '{ODBC Driver 13 for SQL Server}',
        '{SQL Server Native Client 11.0}'
    ]
    
    server = 'SQL01'
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
        query = "EXEC Gestion.dbo.Will_obtener_datos_chatbot_cred @Nro_doc = ?"
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
