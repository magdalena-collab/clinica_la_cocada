from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="veterinaria"
)
cursor = conexion.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT animales.id_animal, animales.nombre, animales.especie, duenios.nombre AS duenio FROM animales JOIN duenios ON animales.id_duenio = duenios.id_duenio")
    animales = cursor.fetchall()
    return render_template('index.html', animales=animales)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        especie = request.form['especie']
        raza = request.form['raza']
        fecha_nacimiento = request.form['fecha_nacimiento']
        id_duenio = request.form['id_duenio']
        cursor.execute("INSERT INTO animales (nombre, especie, raza, fecha_nacimiento, id_duenio) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, especie, raza, fecha_nacimiento, id_duenio))
        conexion.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM duenios")
    duenios = cursor.fetchall()
    return render_template('agregar.html', duenios=duenios)

@app.route('/eliminar/<int:id_animal>')
def eliminar(id_animal):
    cursor.execute("DELETE FROM animales WHERE id_animal = %s", (id_animal,))
    conexion.commit()
    return redirect('/')

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        especie = request.form['especie']
        raza = request.form['raza']
        fecha_nacimiento = request.form['fecha_nacimiento']
        id_duenio = request.form['id_duenio']
        cursor.execute("INSERT INTO animales (nombre, especie, raza, fecha_nacimiento, id_duenio) VALUES (%s, %s, %s, %s, %s)",
                       (nombre, especie, raza, fecha_nacimiento, id_duenio))
        conexion.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM duenios")
    duenios = cursor.fetchall()
    return render_template('agregar.html', duenios=duenios)


if __name__ == '__main__':
    app.run(debug=True)
