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