import mysql.connector
from config import DB_CONFIG


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


class ConsultaModel:

    @staticmethod
    def obtener_todas():
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT *
            FROM consulta
            ORDER BY fecha DESC, hora DESC
        """

        cursor.execute(sql)
        consultas = cursor.fetchall()

        cursor.close()
        conexion.close()

        return consultas

    @staticmethod
    def obtener_por_id(id_consulta):
        conexion = get_db_connection()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM consulta WHERE id_consulta = %s",
            (id_consulta,)
        )

        consulta = cursor.fetchone()

        cursor.close()
        conexion.close()

        return consulta

    @staticmethod
    def agregar(codigo, fecha, hora, id_consulta, motivo, rut):
        conexion = get_db_connection()
        cursor = conexion.cursor()

        sql = """
            INSERT INTO consulta
            (codigo, fecha, hora, id_consulta, motivo, rut)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (codigo, fecha, hora, id_consulta, motivo, rut)
        )

        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar(id_consulta):
        conexion = get_db_connection()
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM consulta WHERE id_consulta = %s",
            (id_consulta,)
        )

        conexion.commit()

        cursor.close()
        conexion.close()