from flask import Blueprint, request, jsonify
from services.atestado_service import AtestadoService
import uuid

atestado_controller = Blueprint('atestado_controller', __name__)
atestado_service = AtestadoService()

@atestado_controller.route('/consultas/<consulta_id>/atestados', methods=['POST'])
def create_atestado(consulta_id):
    data = request.get_json()
    if 'paciente_nome' not in data or 'cid' not in data or 'dias_afastamento' not in data or 'data_inicio' not in data:
        return jsonify({'error': 'Nome do paciente, CID, dias de afastamento e data de início são obrigatórios'}), 400
    
    # Validar se dias_afastamento é um número positivo
    try:
        dias_afastamento = int(data['dias_afastamento'])
        if dias_afastamento <= 0:
            return jsonify({'error': 'Dias de afastamento deve ser um número positivo'}), 400
    except ValueError:
        return jsonify({'error': 'Dias de afastamento deve ser um número válido'}), 400
    
    atestado = atestado_service.create_atestado(
        consulta_id,
        data['paciente_nome'],
        data['cid'],
        dias_afastamento,
        data['data_inicio'],
        data.get('observacoes')
    )
    return jsonify(atestado.to_dict()), 201

@atestado_controller.route('/consultas/<consulta_id>/atestados', methods=['GET'])
def get_atestados(consulta_id):
    atestados = atestado_service.get_all_atestados(consulta_id)
    return jsonify([atestado.to_dict() for atestado in atestados]), 200

@atestado_controller.route('/consultas/<consulta_id>/atestados/<atestado_id>', methods=['GET'])
def get_atestado(consulta_id, atestado_id):
    try:
        uuid.UUID(atestado_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID do atestado deve ser um UUID v4 válido'}), 400
    atestado = atestado_service.get_atestado_by_id(consulta_id, atestado_id)
    if atestado is None:
        return jsonify({'error': 'Atestado não encontrado'}), 404
    return jsonify(atestado.to_dict()), 200

@atestado_controller.route('/consultas/<consulta_id>/atestados/<atestado_id>', methods=['PUT'])
def update_atestado(consulta_id, atestado_id):
    try:
        uuid.UUID(atestado_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID do atestado deve ser um UUID v4 válido'}), 400
    
    data = request.get_json()
    if 'paciente_nome' not in data or 'cid' not in data or 'dias_afastamento' not in data or 'data_inicio' not in data:
        return jsonify({'error': 'Nome do paciente, CID, dias de afastamento e data de início são obrigatórios'}), 400
    
    # Validar se dias_afastamento é um número positivo
    try:
        dias_afastamento = int(data['dias_afastamento'])
        if dias_afastamento <= 0:
            return jsonify({'error': 'Dias de afastamento deve ser um número positivo'}), 400
    except ValueError:
        return jsonify({'error': 'Dias de afastamento deve ser um número válido'}), 400
    
    atestado = atestado_service.update_atestado(
        consulta_id,
        atestado_id,
        data['paciente_nome'],
        data['cid'],
        dias_afastamento,
        data['data_inicio'],
        data.get('observacoes')
    )
    if atestado is None:
        return jsonify({'error': 'Atestado não encontrado'}), 404
    return jsonify(atestado.to_dict()), 200

@atestado_controller.route('/consultas/<consulta_id>/atestados/<atestado_id>', methods=['DELETE'])
def delete_atestado(consulta_id, atestado_id):
    try:
        uuid.UUID(atestado_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID do atestado deve ser um UUID v4 válido'}), 400
    if atestado_service.delete_atestado(consulta_id, atestado_id):
        return jsonify({'message': 'Atestado deletado com sucesso'}), 200
    return jsonify({'error': 'Atestado não encontrado'}), 404

# Endpoints para RH/departamentos
@atestado_controller.route('/rh/atestados', methods=['GET'])
def get_atestados_rh():
    atestados = atestado_service.get_todos_atestados()
    return jsonify([atestado.to_dict_rh() for atestado in atestados]), 200

@atestado_controller.route('/rh/atestados/paciente', methods=['GET'])
def get_atestados_por_paciente():
    """
    Busca atestados por nome do paciente
    Query parameter: nome_paciente
    """
    nome_paciente = request.args.get('nome_paciente')
    
    if not nome_paciente:
        return jsonify({'error': 'Parâmetro nome_paciente é obrigatório'}), 400
    
    # Remove espaços extras e converte para minúsculo para busca flexível
    nome_paciente = nome_paciente.strip()
    
    atestados = atestado_service.get_atestados_by_paciente(nome_paciente)
    return jsonify([atestado.to_dict_rh() for atestado in atestados]), 200

@atestado_controller.route('/rh/atestados/buscar-paciente', methods=['GET'])
def buscar_atestados_paciente():
    """
    Busca atestados por nome do paciente (busca parcial)
    Query parameter: nome
    """
    nome = request.args.get('nome')
    
    if not nome or len(nome.strip()) < 2:
        return jsonify({'error': 'Nome deve ter pelo menos 2 caracteres'}), 400
    
    atestados = atestado_service.buscar_atestados_por_nome_parcial(nome.strip())
    return jsonify([atestado.to_dict_rh() for atestado in atestados]), 200