import sqlite3

# 1. Abrimos la línea telefónica (Establecer la conexión)
conexion = sqlite3.connect('clinica_la_cocada.db')

# 2. Creamos un "mensajero" (cursor) para enviar las ordenes SQL
cursor = conexion.cursor()

# Aquí harías tus consultas... (SELECT, INSERT, etc.)

# 3. Colgamos la línea (Cerrar la conexión)
conexion.close()