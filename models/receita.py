import uuid
from datetime import datetime

class Receita:
    def __init__(self, medicamento, dosagem, paciente_nome, id=None, observacoes=None, duracao=None):
        # Garantir que o ID seja sempre um UUID v4
        self.id = id if id else str(uuid.uuid4())
        self.medicamento = medicamento
        self.dosagem = dosagem
        self.paciente_nome = paciente_nome
        self.observacoes = observacoes
        self.duracao = duracao
        self.data_emissao = datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'medicamento': self.medicamento,
            'dosagem': self.dosagem,
            'paciente_nome': self.paciente_nome,
            'observacoes': self.observacoes,
            'duracao': self.duracao,
            'data_emissao': self.data_emissao
        }
    
    def to_dict_farmacia(self):
        # Versão para farmácia com informações necessárias
        return {
            'receita_id': self.id,
            'medicamento': self.medicamento,
            'dosagem': self.dosagem,
            'paciente_nome': self.paciente_nome,
            'observacoes': self.observacoes,
            'duracao': self.duracao,
            'data_emissao': self.data_emissao
        }