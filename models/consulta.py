import uuid
from datetime import datetime

class Consulta:
    def __init__(self, paciente_nome, medico_nome=None, id=None, data_consulta=None, anamnese=None, diagnostico=None, status="em_andamento"):
        # Garantir que o ID seja sempre um UUID v4
        self.id = id if id else str(uuid.uuid4())
        self.paciente_nome = paciente_nome
        self.medico_nome = medico_nome
        self.data_consulta = data_consulta if data_consulta else datetime.now().isoformat()
        self.anamnese = anamnese
        self.diagnostico = diagnostico
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'paciente_nome': self.paciente_nome,
            'medico_nome': self.medico_nome,
            'data_consulta': self.data_consulta,
            'anamnese': self.anamnese,
            'diagnostico': self.diagnostico,
            'status': self.status
        }
    
    def to_dict_paciente(self):
    
        return {
            'id': self.id,
            'paciente_nome': self.paciente_nome,
            'medico_nome': self.medico_nome,
            'data_consulta': self.data_consulta,  # Já é string, não precisa de isoformat()
            'diagnostico': self.diagnostico,
            'status': self.status
        }