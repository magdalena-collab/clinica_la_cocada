import mysql.connector
from config import DB_CONFIG


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


class TratamientosModel:

    @staticmethod
    def obtener_todos():
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tratamientos")
        tratamientos = cursor.fetchall()

        cursor.close()
        conexion.close()

        return tratamientos

    @staticmethod
    def obtener_por_id(id_tratamiento):
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM tratamientos WHERE id_tratamiento = %s",
            (id_tratamiento,)
        )

        tratamiento = cursor.fetchone()

        cursor.close()
        conexion.close()

        return tratamiento

    @staticmethod
    def agregar(id_tratamiento, nombre, dosis, duracion, id_consulta):
        conexion = get_db_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO tratamientos
            (id_tratamiento, nombre, dosis, duracion, id_consulta)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (id_tratamiento, nombre, dosis, duracion, id_consulta)
        )

        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar(id_tratamiento):
        conexion = get_db_connection()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM tratamientos WHERE id_tratamiento = %s",
            (id_tratamiento,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()