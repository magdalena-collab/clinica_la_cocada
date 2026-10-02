from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="clinica_la_cocada"
)
cursor = conexion.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT paciente.rut, paciente.nombre, paciente.email, tratamiento.nombre AS tratamiento FROM paciente JOIN tratamiento ON tratamiento.rut = tratamiento.id_tratamiento")
    consulta = cursor.fetchall()
    return render_template('index.html', consulta=consulta)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        codigo = request.form ['codigo']
        fecha = request.form['fecha']
        hora =request.form['hora']
        id_consulta = request.form['id_consulta']
        motivo = request.form['motivo']
        nombre= request.form['nombre']
        rut = request.form['rut']
        cursor.execute("INSERT INTO paciente (rut, nombre, apellido, fecha_nacimiento, telefono.email) VALUES (%s, %s, %s, %s, %s)",
                       (rut, codigo, fecha, hora, id_consulta, motivo, nombre ))
        conexion.commit()
        return redirect('/')
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    return render_template('agregar.html', pacientes=pacientes)

@app.route('/eliminar/')
def eliminar(id_consulta):
    cursor.execute("DELETE FROM consulta WHERE id_animal = %s", (id_consulta))
    conexion.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
