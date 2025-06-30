import uuid
from datetime import datetime, timedelta

class Atestado:
    def __init__(self, paciente_nome, cid, dias_afastamento, data_inicio, id=None, observacoes=None):
        # Garantir que o ID seja sempre um UUID v4
        self.id = id if id else str(uuid.uuid4())
        self.paciente_nome = paciente_nome
        self.cid = cid
        self.dias_afastamento = dias_afastamento
        self.data_inicio = data_inicio
        self.observacoes = observacoes
        self.data_emissao = datetime.now().isoformat()
        
        # Calcular data fim baseada na data início e dias de afastamento
        try:
            data_inicio_obj = datetime.fromisoformat(data_inicio.replace('Z', '+00:00'))
            data_fim_obj = data_inicio_obj + timedelta(days=dias_afastamento - 1)  # -1 porque o primeiro dia conta
            self.data_fim = data_fim_obj.isoformat()
        except:
            # Se houver erro na conversão, usar a data atual como fallback
            data_fim_obj = datetime.now() + timedelta(days=dias_afastamento - 1)
            self.data_fim = data_fim_obj.isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'paciente_nome': self.paciente_nome,
            'cid': self.cid,
            'dias_afastamento': self.dias_afastamento,
            'data_inicio': self.data_inicio,
            'data_fim': self.data_fim,
            'observacoes': self.observacoes,
            'data_emissao': self.data_emissao
        }
    
    def to_dict_rh(self):
        # Versão para RH/departamentos com informações necessárias
        return {
            'atestado_id': self.id,
            'paciente_nome': self.paciente_nome,
            'cid': self.cid,
            'dias_afastamento': self.dias_afastamento,
            'data_inicio': self.data_inicio,
            'data_fim': self.data_fim,
            'observacoes': self.observacoes,
            'data_emissao': self.data_emissao
        }