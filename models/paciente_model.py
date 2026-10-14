import mysql.connector
from config import DB_CONFIG


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


class PacienteModel:

    @staticmethod
    def obtener_todos():
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM paciente")
        pacientes = cursor.fetchall()

        cursor.close()
        conexion.close()

        return pacientes

    @staticmethod
    def obtener_por_rut(rut):
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM paciente WHERE rut = %s",
            (rut,)
        )

        paciente = cursor.fetchone()

        cursor.close()
        conexion.close()

        return paciente

    @staticmethod
    def agregar(rut, nombre, apellido, fecha_nacimiento, telefono, email):
        conexion = get_db_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO paciente
            (rut, nombre, apellido, fecha_nacimiento, telefono, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (rut, nombre, apellido, fecha_nacimiento, telefono, email)
        )

        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar(rut):
        conexion = get_db_connection()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM paciente WHERE rut = %s",
            (rut,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()