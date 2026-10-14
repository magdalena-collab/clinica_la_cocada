from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.medico import MedicoModel

medico_bp = Blueprint('medico', __name__, url_prefix='/medicos')


@medico_bp.route('/', methods=['GET'])
def listar_medicos():
    medicos = MedicoModel.obtener_todos()
    return render_template('medicos/index.html', medicos=medicos)



@medico_bp.route('/<int:id>', methods=['GET'])
def detalle_medico(codigo):
  
    medico = MedicoModel.obtener_por_codigo(codigo)
    
    if not medico:
        flash('El médico solicitado no existe.', 'danger')
        return redirect(url_for('medico.listar_medicos'))
        
    return render_template('medicos/detalle.html', medico=medico)


@medico_bp.route('/nuevo', methods=['GET', 'POST'])
def crear_medico():
   
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        especialidad = request.form.get('especialidad')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        codigo =request.form.get('codigo')
        rut=request.form.get('rut')

        if not nombre or not especialidad or not codigo:
            flash('Nombre, especialidad y codigo son obligatorios.', 'warning')
            return render_template('medicos/nuevo.html')

        nuevo_medico = {
            'nombre': nombre,
            'especialidad': especialidad,
            'codigo': codigo,
            'email': email,
            'telefono': telefono,
            'apellido':apellido,
            'rut':rut,
            'estado': 'Activo'
        }

        exito = MedicoModel.crear(nuevo_medico)

        if exito:
            flash('Médico registrado correctamente.', 'success')
            return redirect(url_for('medico.listar_medicos'))
        else:
            flash('Error al registrar el médico. Verifique si el codigo ya existe.', 'danger')

    return render_template('medicos/nuevo.html')


@medico_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar_medico(codigo):

    medico = MedicoModel.obtener_por_id(codigo)

    if not medico:
        flash('Médico no encontrado.', 'danger')
        return redirect(url_for('medico.listar_medicos'))

    if request.method == 'POST':
        datos_actualizados = {
            'nombre': request.form.get('nombre'),
            'especialidad': request.form.get('especialidad'),
            'codigo': request.form.get('codigo'),
            'email': request.form.get('email'),
            'telefono': request.form.get('telefono'),
            'rut': request.form.get('rut'),
            'apellido': request.form.get('apellido')
        }

        MedicoModel.actualizar(codigo, datos_actualizados)
        flash('Información del médico actualizada exitosamente.', 'info')
        return redirect(url_for('medico.detalle_medico', codigo=codigo))

    return render_template('medicos/editar.html', medico=medico)


@medico_bp.route('/<int:id>/cambiar-estado', methods=['POST'])
def cambiar_estado_medico(codigo):
    
    nuevo_estado = request.form.get('estado') # Ej: 'Activo' o 'Inactivo'
    
    if nuevo_estado in ['Activo', 'Inactivo']:
        MedicoModel.cambiar_estado(codigo, nuevo_estado)
        flash(f'El estado del médico ha sido cambiado a {nuevo_estado}.', 'info')
    else:
        flash('Estado no válido.', 'danger')

    return redirect(url_for('medico.listar_medicos'))