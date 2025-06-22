from repositories.receita_repository import ReceitaRepository
from models.receita import Receita

class ReceitaService:
    def __init__(self):
        self.receita_repository = ReceitaRepository()

    def create_receita(self, consulta_id, medicamento, dosagem, paciente_nome, observacoes=None, duracao=None):
        receita = Receita(
            medicamento=medicamento,
            dosagem=dosagem,
            paciente_nome=paciente_nome,
            observacoes=observacoes,
            duracao=duracao
        )
        return self.receita_repository.add_receita(consulta_id, receita)

    def get_all_receitas(self, consulta_id):
        return self.receita_repository.get_all_receitas(consulta_id)

    def get_receita_by_id(self, consulta_id, receita_id):
        return self.receita_repository.get_receita_by_id(consulta_id, receita_id)

    def get_todas_receitas(self):
        """
        Retorna todas as receitas para a farmácia
        """
        return self.receita_repository.get_todas_receitas()

    def get_receitas_by_paciente(self, nome_paciente):
        """
        Retorna receitas de um paciente específico
        """
        return self.receita_repository.get_receitas_by_paciente(nome_paciente)

    def buscar_receitas_por_nome_parcial(self, nome_parcial):
        """
        Busca receitas por nome parcial do paciente (mais flexível)
        """
        return self.receita_repository.buscar_receitas_por_nome_parcial(nome_parcial)

    def update_receita(self, consulta_id, receita_id, medicamento, dosagem, observacoes=None, duracao=None):
        return self.receita_repository.update_receita(consulta_id, receita_id, medicamento, dosagem, observacoes, duracao)

    def delete_receita(self, consulta_id, receita_id):
        return self.receita_repository.delete_receita(consulta_id, receita_id)