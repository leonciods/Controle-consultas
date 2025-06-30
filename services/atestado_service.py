from repositories.atestado_repository import AtestadoRepository
from models.atestado import Atestado

class AtestadoService:
    def __init__(self):
        self.atestado_repository = AtestadoRepository()

    def create_atestado(self, consulta_id, paciente_nome, cid, dias_afastamento, data_inicio, observacoes=None):
        atestado = Atestado(
            paciente_nome=paciente_nome,
            cid=cid,
            dias_afastamento=dias_afastamento,
            data_inicio=data_inicio,
            observacoes=observacoes
        )
        return self.atestado_repository.add_atestado(consulta_id, atestado)

    def get_all_atestados(self, consulta_id):
        return self.atestado_repository.get_all_atestados(consulta_id)

    def get_atestado_by_id(self, consulta_id, atestado_id):
        return self.atestado_repository.get_atestado_by_id(consulta_id, atestado_id)

    def get_todos_atestados(self):
        """
        Retorna todos os atestados para RH/departamentos
        """
        return self.atestado_repository.get_todos_atestados()

    def get_atestados_by_paciente(self, nome_paciente):
        """
        Retorna atestados de um paciente específico
        """
        return self.atestado_repository.get_atestados_by_paciente(nome_paciente)

    def buscar_atestados_por_nome_parcial(self, nome_parcial):
        """
        Busca atestados por nome parcial do paciente (mais flexível)
        """
        return self.atestado_repository.buscar_atestados_por_nome_parcial(nome_parcial)

    def update_atestado(self, consulta_id, atestado_id, paciente_nome, cid, dias_afastamento, data_inicio, observacoes=None):
        return self.atestado_repository.update_atestado(consulta_id, atestado_id, paciente_nome, cid, dias_afastamento, data_inicio, observacoes)

    def delete_atestado(self, consulta_id, atestado_id):
        return self.atestado_repository.delete_atestado(consulta_id, atestado_id)