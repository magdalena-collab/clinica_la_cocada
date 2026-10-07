import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    """Establece y retorna la conexión a la base de datos."""
    return mysql.connector.connect(**DB_CONFIG)

class ClinicaModel:
    
    @staticmethod
    def obtener_informacion():
        """Obtiene la información general de la clínica (por ejemplo, el primer registro de la tabla)."""
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM clinica LIMIT 1")
        clinica = cursor.fetchone()
        cursor.close()
        conexion.close()
        return clinica

    @staticmethod
    def actualizar_informacion(clinica_id, nombre, direccion, telefono, email):
        """Actualiza los datos principales de la clínica."""
        conexion = get_db_connection()
        cursor = conexion.cursor()
        sql = """
            UPDATE clinica 
            SET nombre = %s, direccion = %s, telefono = %s, email = %s 
            WHERE id = %s
        """
        cursor.execute(sql, (nombre, direccion, telefono, email, clinica_id))
        conexion.commit()
        cursor.close()
        conexion.close()