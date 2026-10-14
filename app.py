from flask import Flask, render_template, request, redirect, url_for

from models.paciente_model import PacienteModel
from models.consulta_model import ConsultaModel
from models.tratamientos_model import TratamientosModel
from models.clinica_model import ClinicaModel


app = Flask(__name__)


@app.route('/')
def index():
    pacientes = PacienteModel.obtener_todos()
    consultas = ConsultaModel.obtener_todas()
    tratamientos = TratamientosModel.obtener_todos()
    clinica = ClinicaModel.obtener_informacion()

    return render_template(
        'index.html',
        pacientes=pacientes,
        consultas=consultas,
        tratamientos=tratamientos,
        clinica=clinica
    )


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():

    if request.method == 'POST':

        rut = request.form['rut']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha_nacimiento = request.form['fecha_nacimiento']
        telefono = request.form['telefono']
        email = request.form['email']

        PacienteModel.agregar(
            rut,
            nombre,
            apellido,
            fecha_nacimiento,
            telefono,
            email
        )

        return redirect(url_for('index'))

    pacientes = PacienteModel.obtener_todos()

    return render_template(
        'agregar.html',
        pacientes=pacientes
    )


@app.route('/eliminar/<rut>')
def eliminar_paciente(rut):

    PacienteModel.eliminar(rut)

    return redirect(url_for('index'))


@app.route('/eliminar_consulta/<int:id_consulta>')
def eliminar_consulta(id_consulta):

    ConsultaModel.eliminar(id_consulta)

    return redirect(url_for('index'))


@app.route('/clinica')
def clinica():

    informacion = ClinicaModel.obtener_informacion()

    return render_template(
        'clinica.html',
        clinica=informacion
    )


@app.route('/actualizar_clinica', methods=['POST'])
def actualizar_clinica():

    clinica_id = request.form['clinica_id']
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    email = request.form['email']

    ClinicaModel.actualizar_informacion(
        clinica_id,
        nombre,
        direccion,
        telefono,
        email
    )

    return redirect(url_for('clinica'))


if __name__ == '__main__':
    app.run(debug=True)
