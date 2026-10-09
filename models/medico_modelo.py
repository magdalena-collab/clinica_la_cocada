import mysql.connector
from config import DB_CONFIG


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


class MedicoModel:

    @staticmethod
    def obtener_todos():
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM medico")
        medicos = cursor.fetchall()

        cursor.close()
        conexion.close()

        return medicos

    @staticmethod
    def obtener_por_id(id_medico):
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM medico WHERE id_medico = %s",
            (id_medico,)
        )

        medico = cursor.fetchone()

        cursor.close()
        conexion.close()

        return medico

    @staticmethod
    def agregar(id_medico, nombre, apellido, especialidad, telefono, email):
        conexion = get_db_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO medico
            (id_medico, nombre, apellido, especialidad, telefono, email)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (id_medico, nombre, apellido, especialidad, telefono, email)
        )

        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar(id_medico):
        conexion = get_db_connection()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM medico WHERE id_medico = %s",
            (id_medico,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()