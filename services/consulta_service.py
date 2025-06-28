from repositories.consulta_repository import ConsultaRepository
from models.consulta import Consulta

class ConsultaService:
    def __init__(self):
        self.consulta_repository = ConsultaRepository()

    def create_consulta(self, paciente_nome, medico_nome=None, anamnese=None, diagnostico=None, status="em_andamento"):
        consulta = Consulta(
            paciente_nome=paciente_nome,
            medico_nome=medico_nome,
            anamnese=anamnese,
            diagnostico=diagnostico,
            status=status
        )
        return self.consulta_repository.add_consulta(consulta)

    def get_all_consultas(self):
        return self.consulta_repository.get_all_consultas()

    def get_consulta_by_id(self, consulta_id):
        return self.consulta_repository.get_consulta_by_id(consulta_id)

    def update_consulta(self, consulta_id, paciente_nome, medico_nome=None, anamnese=None, diagnostico=None, status=None):
        return self.consulta_repository.update_consulta(consulta_id, paciente_nome, medico_nome, anamnese, diagnostico, status)

    def delete_consulta(self, consulta_id):
        return self.consulta_repository.delete_consulta(consulta_id)
    
    def get_consultas_by_paciente(self, nome_paciente):
        """Busca consultas por nome exato do paciente"""
        todas_consultas = self.get_all_consultas()
        return [consulta for consulta in todas_consultas if consulta.paciente_nome.lower() == nome_paciente.lower()]

    def buscar_consultas_por_nome_parcial(self, nome_parcial):
        """Busca consultas por nome parcial do paciente"""
        todas_consultas = self.get_all_consultas()
        nome_parcial = nome_parcial.lower()
        return [consulta for consulta in todas_consultas if nome_parcial in consulta.paciente_nome.lower()]

    def get_consultas_by_status(self, status):
        """Busca consultas por status"""
        todas_consultas = self.get_all_consultas()
        return [consulta for consulta in todas_consultas if consulta.status == status]

    def get_consultas_by_medico(self, nome_medico):
        """Busca consultas por nome do médico"""
        todas_consultas = self.get_all_consultas()
        return [consulta for consulta in todas_consultas if consulta.medico_nome and consulta.medico_nome.lower() == nome_medico.lower()]