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
        
    return render_template('pacientes/detalle.html', paciente=paciente)



@paciente_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_paciente():
    """
    Lógica de control según método HTTP:
    - GET: Renderiza el formulario de registro.
    - POST: Extrae los datos recibidos, valida y le pide al Modelo guardarlos.
    """
    if request.method == 'POST':
        # Captura de datos enviados mediante la petición HTTP
        nombre = request.form.get('nombre')
        rut_dni = request.form.get('rut_dni')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        telefono = request.form.get('telefono')

        # Lógica de validación rápida
        if not nombre or not rut_dni:
            flash('El nombre y documento de identidad son obligatorios.', 'warning')
            return render_template('pacientes/nuevo.html')

        # Interacción con el Modelo para persistir los datos
        exito = PacienteModel.crear({
            'nombre': nombre,
            'rut_dni': rut_dni,
            'fecha_nacimiento': fecha_nacimiento,
            'telefono': telefono
        })

        if exito:
            flash('Paciente registrado exitosamente.', 'success')
            return redirect(url_for('paciente.listar_pacientes'))
        else:
            flash('Ocurrió un error al registrar al paciente.', 'danger')

    # Si es GET, simplemente mostramos la vista con el formulario
    return render_template('pacientes/nuevo.html')


# ---------------------------------------------------------
# 4. EDITAR UN PACIENTE (GET / POST)
# ---------------------------------------------------------
@paciente_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_paciente(id):
    """
    Orquestación para actualizar un registro existente.
    """
    paciente = PacienteModel.obtener_por_id(id)

    if not paciente:
        flash('Paciente no encontrado.', 'danger')
        return redirect(url_for('paciente.listar_pacientes'))

    if request.method == 'POST':
        datos_actualizados = {
            'nombre': request.form.get('nombre'),
            'rut_dni': request.form.get('rut_dni'),
            'fecha_nacimiento': request.form.get('fecha_nacimiento'),
            'telefono': request.form.get('telefono')
        }

        # Actualizamos llamando al Modelo
        PacienteModel.actualizar(id, datos_actualizados)
        flash('Datos del paciente actualizados.', 'info')
        return redirect(url_for('paciente.detalle_paciente', id=id))

    return render_template('pacientes/editar.html', paciente=paciente)


# ---------------------------------------------------------
# 5. ELIMINAR UN PACIENTE (POST / DELETE)
# ---------------------------------------------------------
@paciente_bp.route('/<int:id>/eliminar', methods=['POST'])
def eliminar_paciente(id):
    """
    Orquestación: Llama al Modelo para eliminar o desactivar el registro
    y redirige a la lista general.
    """
    exito = PacienteModel.eliminar(id)
    
    if exito:
        flash('Paciente eliminado con éxito.', 'success')
    else:
        flash('No se pudo eliminar al paciente.', 'danger')

    return redirect(url_for('paciente.listar_pacientes'))