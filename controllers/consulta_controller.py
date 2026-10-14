from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify

from consulta_modelo import ConsultaModel
from paciente_modelo import PacienteModel
from medico_modelo import MedicoModel

consulta_bp = Blueprint('consulta', __name__, url_prefix='/consultas')



@consulta_bp.route('/', methods=['GET'])
def listar_consultas():
    
    consultas = Consulta_modelo.obtener_todas()
    return render_template('consultas/index.html', consultas=consultas)



@consulta_bp.route('/<int:id>', methods=['GET'])
def detalle_consulta(id):
   
    consulta = Consulta_modelo.obtener_por_id(id)
    
    if not consulta:
        flash('La consulta médica especificada no existe.', 'danger')
        return redirect(url_for('consulta.listar_consultas'))
        
    return render_template('consultas/detalle.html', consulta=consulta)



@consulta_bp.route('/nueva', methods=['GET', 'POST'])
def crear_consulta():
    
    if request.method == 'POST':
        rut = request.form.get('rut')
        codigo = request.form.get('codigo')
        fecha = request.form.get('fecha')
        motivo = request.form.get('motivo')
        hora=request.form.get('hora')
        id_consulta=request.form.get('id_consulta')

       
        if not rut or not codigo or not fecha or not hora:
            flash('Debe seleccionar paciente, médico, fecha y hora.', 'warning')
            return redirect(url_for('consulta.crear_consulta'))

       
        nueva_consulta = {
            'rut': rut,
            'codigo': codigo,
            'fecha': fecha,
            'motivo': motivo,
            'hora':hora,
            'id_consulta':id_consulta,
            'estado': 'Programada'
        }
        
        exito = consulta_modelo.crear(nueva_consulta)

        if exito:
            flash('Consulta agendada con éxito.', 'success')
            return redirect(url_for('consulta.listar_consultas'))
        else:
            flash('No se pudo agendar la consulta. Verifique disponibilidad.', 'danger')

    
    pacientes = paciente_modelo.obtener_todos()
    medicos = medico_modelo.obtener_activos()
    
    return render_template('consultas/nueva.html', pacientes=pacientes, medicos=medicos)



@consulta_bp.route('/<int:id>/atender', methods=['GET', 'POST'])
def atender_consulta(id):
    
    consulta = Consulta_modelo.obtener_por_id(id)

    if not consulta:
        flash('Consulta no encontrada.', 'danger')
        return redirect(url_for('consulta.listar_consultas'))

    if request.method == 'POST':
        tratamiento = request.form.get('tratamiento')

        datos_atencion = {
            'tratamiento': tratamiento,
            'estado': 'Realizada'
        }

        consulta_modelo.actualizar_atencion(id, datos_atencion)
        flash('Atención médica registrada correctamente.', 'success')
        return redirect(url_for('consulta.detalle_consulta', id=id))

    return render_template('consultas/editar.html', consulta=consulta)



@consulta_bp.route('/<int:id>/cancelar', methods=['POST'])
def cancelar_consulta(id):
    
    exito = consulta_modelo.cambiar_estado(id, 'Cancelada')
    
    if exito:
        flash('La consulta ha sido cancelada.', 'info')
    else:
        flash('Ocurrió un error al intentar cancelar.', 'danger')

    return redirect(url_for('consulta.listar_consultas'))