from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from tratamiento_modelo import TratamientoModel
from consulta_modelo import ConsultaModel
from paciente_modelo import PacienteModel

tratamiento_bp = Blueprint('tratamiento', __name__, url_prefix='/tratamientos')


@tratamiento_bp.route('/', methods=['GET'])
def listar_tratamientos():
    
    tratamientos = TratamientoModel.obtener_todos()
    return render_template('tratamientos/index.html', tratamientos=tratamientos)


@tratamiento_bp.route('/paciente/<int:rut>', methods=['GET'])
def tratamientos_por_paciente(rut):
   
    paciente = PacienteModel.obtener_por_id(rut)
    
    if not paciente:
        flash('El paciente especificado no existe.', 'danger')
        return redirect(url_for('tratamiento.listar_tratamientos'))

    tratamientos = TratamientoModel.obtener_por_paciente(rut)
    return render_template(
        'tratamientos/index.html', 
        paciente=paciente, 
        tratamientos=tratamientos
    )


@tratamiento_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_tratamiento():
   
    if request.method == 'POST':
        id_consulta = request.form.get('id_consulta')
        dosis = request.form.get('dosis')
        nombre = request.form.get('nombre')
        duracion = request.form.get('duracion')


        if not id_consulta or not nombre:
            flash('la consulta y el nombre del tratamiento son obligatorios.', 'warning')
            return redirect(url_for('tratamiento.crear_tratamiento'))

        nuevo_tratamiento = {
            'id_consulta': id_consulta or None,
            'nombre': nombre,
            'dosis': dosis,
            'duracion': duracion,
            'estado': 'Activo'
        }

        exito = TratamientoModel.crear(nuevo_tratamiento)

        if exito:
            flash('Tratamiento registrado correctamente.', 'success')
            return redirect(url_for('tratamiento.tratamientos_por_paciente', id_consulta=id_consulta))
        else:
            flash('Error al guardar el tratamiento.', 'danger')

    pacientes = PacienteModel.obtener_todos()
    consultas = ConsultaModel.obtener_todas()
    
    return render_template('tratamientos/nuevo.html', pacientes=pacientes, consultas=consultas)



@tratamiento_bp.route('/<int:id>/cambiar-estado', methods=['POST'])
def cambiar_estado(id):
    
    nuevo_estado = request.form.get('estado') # Ej: 'Completado', 'Suspendido'
    id_consulta = request.form.get('id_consulta')

    if nuevo_estado in ['Activo', 'Completado', 'Suspendido']:
        TratamientoModel.actualizar_estado(id, nuevo_estado)
        flash(f'El estado del tratamiento se actualizó a {nuevo_estado}.', 'info')
    else:
        flash('Estado no válido.', 'danger')

    if id_consulta:
        return redirect(url_for('tratamiento.tratamientos_por_paciente', id_consulta=id_consulta))
    return redirect(url_for('tratamiento.listar_tratamientos'))