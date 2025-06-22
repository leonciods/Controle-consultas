from firestore.firebase_config import init_firebase
from models.consulta import Consulta
import uuid

class ConsultaRepository:
    def __init__(self):
        self.db = init_firebase()

    def add_consulta(self, consulta):
        # Usar o ID UUID v4 gerado pela classe Consulta
        doc_ref = self.db.collection('consultas').document(consulta.id)
        doc_ref.set(consulta.to_dict())
        return consulta

    def get_all_consultas(self):
        collection = self.db.collection('consultas')
        return [
            Consulta(
                paciente_nome=doc.get('paciente_nome'),
                medico_nome=doc.get('medico_nome'),
                id=doc.id,
                data_consulta=doc.get('data_consulta'),
                anamnese=doc.get('anamnese'),
                diagnostico=doc.get('diagnostico'),
                status=doc.get('status')
            ) for doc in collection.stream()
        ]

    def get_consulta_by_id(self, consulta_id):
        # Validar se consulta_id é um UUID v4 válido
        try:
            uuid.UUID(consulta_id, version=4)
        except ValueError:
            return None
        doc = self.db.collection('consultas').document(consulta_id).get()
        if doc.exists:
            return Consulta(
                paciente_nome=doc.get('paciente_nome'),
                medico_nome=doc.get('medico_nome'),
                id=doc.id,
                data_consulta=doc.get('data_consulta'),
                anamnese=doc.get('anamnese'),
                diagnostico=doc.get('diagnostico'),
                status=doc.get('status')
            )
        return None

    def update_consulta(self, consulta_id, paciente_nome, medico_nome=None, anamnese=None, diagnostico=None, status=None):
        # Validar se consulta_id é um UUID v4 válido
        try:
            uuid.UUID(consulta_id, version=4)
        except ValueError:
            return None
        doc_ref = self.db.collection('consultas').document(consulta_id)
        if doc_ref.get().exists:
            consulta = Consulta(
                paciente_nome=paciente_nome,
                medico_nome=medico_nome,
                id=consulta_id,
                anamnese=anamnese,
                diagnostico=diagnostico,
                status=status
            )
            doc_ref.set(consulta.to_dict())
            return consulta
        return None

    def delete_consulta(self, consulta_id):
        # Validar se consulta_id é um UUID v4 válido
        try:
            uuid.UUID(consulta_id, version=4)
        except ValueError:
            return False
        doc_ref = self.db.collection('consultas').document(consulta_id)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False