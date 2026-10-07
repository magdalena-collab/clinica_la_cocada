import mysql.connector
from config import DB_CONFIG  # Asegúrate de tener tus credenciales en config.py

def get_db_connection():
    """Establece y retorna la conexión a la base de datos."""
    return mysql.connector.connect(**DB_CONFIG)

class PacienteModel:
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los registros de la tabla pacientes."""
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pacientes")
        pacientes = cursor.fetchall()
        cursor.close()
        conexion.close()
        return pacientes

    @staticmethod
    def obtener_por_id(paciente_id):
        """Obtiene un paciente por su ID."""
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pacientes WHERE id = %s", (paciente_id,))
        paciente = cursor.fetchone()
        cursor.close()
        conexion.close()
        return paciente

    @staticmethod
    def crear(nombre, edad, diagnostico):
        """Inserta un nuevo paciente en la base de datos."""
        conexion = get_db_connection()
        cursor = conexion.cursor()
        sql = "INSERT INTO pacientes (nombre, edad, diagnostico) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, edad, diagnostico))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def actualizar(paciente_id, nombre, edad, diagnostico):
        """Actualiza la información de un paciente existente."""
        conexion = get_db_connection()
        cursor = conexion.cursor()
        sql = "UPDATE pacientes SET nombre = %s, edad = %s, diagnostico = %s WHERE id = %s"
        cursor.execute(sql, (nombre, edad, diagnostico, paciente_id))
        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar(paciente_id):
        """Elimina un paciente según su ID."""
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM pacientes WHERE id = %s", (paciente_id,))
        conexion.commit()
        cursor.close()
        conexion.close()