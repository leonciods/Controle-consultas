from flask import Blueprint, request, jsonify
from services.consulta_service import ConsultaService
import uuid

consulta_controller = Blueprint('consulta_controller', __name__)
consulta_service = ConsultaService()

@consulta_controller.route('/consultas', methods=['POST'])
def create_consulta():
    data = request.get_json()
    if 'paciente_nome' not in data:
        return jsonify({'error': 'Nome do paciente é obrigatório'}), 400
    consulta = consulta_service.create_consulta(
        data['paciente_nome'],
        data.get('medico_nome'),
        data.get('anamnese'),
        data.get('diagnostico'),
        data.get('status', 'em_andamento')
    )
    return jsonify(consulta.to_dict()), 201

@consulta_controller.route('/consultas', methods=['GET'])
def get_consultas():
    consultas = consulta_service.get_all_consultas()
    return jsonify([consulta.to_dict() for consulta in consultas]), 200

@consulta_controller.route('/consultas/<consulta_id>', methods=['GET'])
def get_consulta(consulta_id):
    try:
        uuid.UUID(consulta_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID da consulta deve ser um UUID v4 válido'}), 400
    consulta = consulta_service.get_consulta_by_id(consulta_id)
    if consulta is None:
        return jsonify({'error': 'Consulta não encontrada'}), 404
    return jsonify(consulta.to_dict()), 200

@consulta_controller.route('/consultas/<consulta_id>', methods=['PUT'])
def update_consulta(consulta_id):
    try:
        uuid.UUID(consulta_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID da consulta deve ser um UUID v4 válido'}), 400
    data = request.get_json()
    if 'paciente_nome' not in data:
        return jsonify({'error': 'Nome do paciente é obrigatório'}), 400
    consulta = consulta_service.update_consulta(
        consulta_id,
        data['paciente_nome'],
        data.get('medico_nome'),
        data.get('anamnese'),
        data.get('diagnostico'),
        data.get('status')
    )
    if consulta is None:
        return jsonify({'error': 'Consulta não encontrada'}), 404
    return jsonify(consulta.to_dict()), 200

@consulta_controller.route('/consultas/<consulta_id>', methods=['DELETE'])
def delete_consulta(consulta_id):
    try:
        uuid.UUID(consulta_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID da consulta deve ser um UUID v4 válido'}), 400
    if consulta_service.delete_consulta(consulta_id):
        return jsonify({'message': 'Consulta deletada com sucesso'}), 200
    return jsonify({'error': 'Consulta não encontrada'}), 404



# Endpoints para API do paciente
@consulta_controller.route('/paciente/consultas', methods=['GET'])
def get_consultas_paciente():
    """
    Retorna todas as consultas para visualização do paciente
    """
    consultas = consulta_service.get_all_consultas()
    return jsonify([consulta.to_dict_paciente() for consulta in consultas]), 200

@consulta_controller.route('/paciente/consultas/nome', methods=['GET'])
def get_consultas_por_nome_paciente():
    """
    Busca consultas por nome do paciente
    Query parameter: nome_paciente
    """
    nome_paciente = request.args.get('nome_paciente')
    
    if not nome_paciente:
        return jsonify({'error': 'Parâmetro nome_paciente é obrigatório'}), 400
    
    nome_paciente = nome_paciente.strip()
    
    consultas = consulta_service.get_consultas_by_paciente(nome_paciente)
    return jsonify([consulta.to_dict_paciente() for consulta in consultas]), 200

@consulta_controller.route('/paciente/consultas/buscar-nome', methods=['GET'])
def buscar_consultas_paciente():
    """
    Busca consultas por nome do paciente (busca parcial)
    Query parameter: nome
    """
    nome = request.args.get('nome')
    
    if not nome or len(nome.strip()) < 2:
        return jsonify({'error': 'Nome deve ter pelo menos 2 caracteres'}), 400
    
    consultas = consulta_service.buscar_consultas_por_nome_parcial(nome.strip())
    return jsonify([consulta.to_dict_paciente() for consulta in consultas]), 200

@consulta_controller.route('/paciente/consultas/<consulta_id>', methods=['GET'])
def get_consulta_paciente(consulta_id):
    """
    Retorna uma consulta específica para visualização do paciente
    """
    try:
        uuid.UUID(consulta_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID da consulta deve ser um UUID v4 válido'}), 400
    
    consulta = consulta_service.get_consulta_by_id(consulta_id)
    if consulta is None:
        return jsonify({'error': 'Consulta não encontrada'}), 404
    
    return jsonify(consulta.to_dict_paciente()), 200

@consulta_controller.route('/paciente/consultas/status/<status>', methods=['GET'])
def get_consultas_por_status_paciente(status):
    """
    Busca consultas por status para visualização do paciente
    Status possíveis: em_andamento, finalizada, cancelada
    """
    status_validos = ['em_andamento', 'finalizada', 'cancelada']
    
    if status not in status_validos:
        return jsonify({'error': f'Status deve ser um dos seguintes: {", ".join(status_validos)}'}), 400
    
    consultas = consulta_service.get_consultas_by_status(status)
    return jsonify([consulta.to_dict_paciente() for consulta in consultas]), 200

@consulta_controller.route('/paciente/consultas/medico', methods=['GET'])
def get_consultas_por_medico_paciente():
    """
    Busca consultas por nome do médico para visualização do paciente
    Query parameter: nome_medico
    """
    nome_medico = request.args.get('nome_medico')
    
    if not nome_medico:
        return jsonify({'error': 'Parâmetro nome_medico é obrigatório'}), 400
    
    nome_medico = nome_medico.strip()
    
    consultas = consulta_service.get_consultas_by_medico(nome_medico)
    return jsonify([consulta.to_dict_paciente() for consulta in consultas]), 200