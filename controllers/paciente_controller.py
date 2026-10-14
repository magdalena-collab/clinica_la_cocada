from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from models.paciente import PacienteModel

paciente_bp = Blueprint('paciente', __name__, url_prefix='/pacientes')

@paciente_bp.route('/', methods=['GET'])
def listar_pacientes():
    pacientes = PacienteModel.obtener_todos()
    return render_template('paciente/index.html', pacientes=pacientes)


@paciente_bp.route('/<int:id>', methods=['GET'])
def detalle_paciente(id):
    paciente = PacienteModel.obtener_por_id(id)
    
    if not paciente:
        flash('El paciente solicitado no existe.', 'danger')
        return redirect(url_for('paciente.listar_pacientes'))
        
    return render_template('pacientes/editar.html', paciente=paciente)



@paciente_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_paciente():
   
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        rut = request.form.get('rut')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        telefono = request.form.get('telefono')
        apellido=request.form.get('apellido')
        email=request.form.get('email')

        if not nombre or not rut:
            flash('El nombre y documento de identidad son obligatorios.', 'warning')
            return render_template('pacientes/crear.html')

        exito = PacienteModel.crear({
            'nombre': nombre,
            'rut': rut,
            'fecha_nacimiento': fecha_nacimiento,
            'telefono': telefono,
            'apellido':apellido,
            'email':email
        })

        if exito:
            flash('Paciente registrado exitosamente.', 'success')
            return redirect(url_for('paciente.listar_pacientes'))
        else:
            flash('Ocurrió un error al registrar al paciente.', 'danger')

    return render_template('pacientes/index.html')



@paciente_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_paciente(id):

    paciente = PacienteModel.obtener_por_id(id)

    if not paciente:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('paciente.listar_pacientes'))

    if request.method == 'POST':
        datos_actualizados = {
            'nombre': request.form.get('nombre'),
            'rut': request.form.get('rut'),
            'fecha_nacimiento': request.form.get('fecha_nacimiento'),
            'telefono': request.form.get('telefono'),
            'apellido': request.form.get('apellido'),
            'email': request.form.get('email')
        }

    
        PacienteModel.actualizar(id, datos_actualizados)
        flash('Datos del paciente actualizados.', 'info')
        return redirect(url_for('paciente.detalle_paciente', id=id))

    return render_template('pacientes/editar.html', paciente=paciente)



@paciente_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_paciente(id):
 
    exito = PacienteModel.eliminar(id)
    
    if exito:
        flash('Paciente eliminado con éxito.', 'success')
    else:
        flash('No se pudo eliminar al paciente.', 'danger')

    return redirect(url_for('paciente.listar_pacientes'))