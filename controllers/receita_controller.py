from flask import Blueprint, request, jsonify
from services.receita_service import ReceitaService
import uuid

receita_controller = Blueprint('receita_controller', __name__)
receita_service = ReceitaService()

@receita_controller.route('/consultas/<consulta_id>/receitas', methods=['POST'])
def create_receita(consulta_id):
    data = request.get_json()
    if 'medicamento' not in data or 'dosagem' not in data or 'paciente_nome' not in data:
        return jsonify({'error': 'Medicamento, dosagem e nome do paciente são obrigatórios'}), 400
    receita = receita_service.create_receita(
        consulta_id,
        data['medicamento'],
        data['dosagem'],
        data['paciente_nome'],
        data.get('observacoes'),
        data.get('duracao')
    )
    return jsonify(receita.to_dict()), 201

@receita_controller.route('/consultas/<consulta_id>/receitas', methods=['GET'])
def get_receitas(consulta_id):
    receitas = receita_service.get_all_receitas(consulta_id)
    return jsonify([receita.to_dict() for receita in receitas]), 200

@receita_controller.route('/consultas/<consulta_id>/receitas/<receita_id>', methods=['GET'])
def get_receita(consulta_id, receita_id):
    try:
        uuid.UUID(receita_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID da receita deve ser um UUID v4 válido'}), 400
    receita = receita_service.get_receita_by_id(consulta_id, receita_id)
    if receita is None:
        return jsonify({'error': 'Receita não encontrada'}), 404
    return jsonify(receita.to_dict()), 200

@receita_controller.route('/consultas/<consulta_id>/receitas/<receita_id>', methods=['PUT'])
def update_receita(consulta_id, receita_id):
    try:
        uuid.UUID(receita_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID da receita deve ser um UUID v4 válido'}), 400
    data = request.get_json()
    if 'medicamento' not in data or 'dosagem' not in data:
        return jsonify({'error': 'Medicamento e dosagem são obrigatórios'}), 400
    receita = receita_service.update_receita(
        consulta_id,
        receita_id,
        data['medicamento'],
        data['dosagem'],
        data.get('observacoes'),
        data.get('duracao')
    )
    if receita is None:
        return jsonify({'error': 'Receita não encontrada'}), 404
    return jsonify(receita.to_dict()), 200

@receita_controller.route('/consultas/<consulta_id>/receitas/<receita_id>', methods=['DELETE'])
def delete_receita(consulta_id, receita_id):
    try:
        uuid.UUID(receita_id, version=4)
    except ValueError:
        return jsonify({'error': 'ID da receita deve ser um UUID v4 válido'}), 400
    if receita_service.delete_receita(consulta_id, receita_id):
        return jsonify({'message': 'Receita deletada com sucesso'}), 200
    return jsonify({'error': 'Receita não encontrada'}), 404

# Endpoints para farmácia
@receita_controller.route('/farmacia/receitas', methods=['GET'])
def get_receitas_farmacia():
    receitas = receita_service.get_todas_receitas()
    return jsonify([receita.to_dict_farmacia() for receita in receitas]), 200

@receita_controller.route('/farmacia/receitas/paciente', methods=['GET'])
def get_receitas_por_paciente():
    """
    Busca receitas por nome do paciente
    Query parameter: nome_paciente
    """
    nome_paciente = request.args.get('nome_paciente')
    
    if not nome_paciente:
        return jsonify({'error': 'Parâmetro nome_paciente é obrigatório'}), 400
    
    # Remove espaços extras e converte para minúsculo para busca flexível
    nome_paciente = nome_paciente.strip()
    
    receitas = receita_service.get_receitas_by_paciente(nome_paciente)
    return jsonify([receita.to_dict_farmacia() for receita in receitas]), 200

@receita_controller.route('/farmacia/receitas/buscar-paciente', methods=['GET'])
def buscar_receitas_paciente():
    """
    Busca receitas por nome do paciente (busca parcial)
    Query parameter: nome
    """
    nome = request.args.get('nome')
    
    if not nome or len(nome.strip()) < 2:
        return jsonify({'error': 'Nome deve ter pelo menos 2 caracteres'}), 400
    
    receitas = receita_service.buscar_receitas_por_nome_parcial(nome.strip())
    return jsonify([receita.to_dict_farmacia() for receita in receitas]), 200