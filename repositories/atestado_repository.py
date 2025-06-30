from firestore.firebase_config import init_firebase
from models.atestado import Atestado
import uuid

class AtestadoRepository:
    def __init__(self):
        self.db = init_firebase()

    def add_atestado(self, consulta_id, atestado):
        # Usar o ID UUID v4 gerado pela classe Atestado
        collection = self.db.collection('consultas').document(consulta_id).collection('atestados')
        doc_ref = collection.document(atestado.id)
        doc_ref.set(atestado.to_dict())
        return atestado

    def get_all_atestados(self, consulta_id):
        collection = self.db.collection('consultas').document(consulta_id).collection('atestados')
        return [
            Atestado(
                paciente_nome=doc.get('paciente_nome'),
                cid=doc.get('cid'),
                dias_afastamento=doc.get('dias_afastamento'),
                data_inicio=doc.get('data_inicio'),
                id=doc.id,
                observacoes=doc.get('observacoes')
            ) for doc in collection.stream()
        ]

    def get_atestado_by_id(self, consulta_id, atestado_id):
        # Validar se atestado_id é um UUID v4 válido
        try:
            uuid.UUID(atestado_id, version=4)
        except ValueError:
            return None
        doc = self.db.collection('consultas').document(consulta_id).collection('atestados').document(atestado_id).get()
        if doc.exists:
            return Atestado(
                paciente_nome=doc.get('paciente_nome'),
                cid=doc.get('cid'),
                dias_afastamento=doc.get('dias_afastamento'),
                data_inicio=doc.get('data_inicio'),
                id=doc.id,
                observacoes=doc.get('observacoes')
            )
        return None

    def get_todos_atestados(self):
        # Busca todos os atestados de todas as consultas (para RH/departamentos)
        todos_atestados = []
        consultas = self.db.collection('consultas').stream()
        
        for consulta in consultas:
            atestados = self.db.collection('consultas').document(consulta.id).collection('atestados').stream()
            for atestado in atestados:
                todos_atestados.append(
                    Atestado(
                        paciente_nome=atestado.get('paciente_nome'),
                        cid=atestado.get('cid'),
                        dias_afastamento=atestado.get('dias_afastamento'),
                        data_inicio=atestado.get('data_inicio'),
                        id=atestado.id,
                        observacoes=atestado.get('observacoes')
                    )
                )
        return todos_atestados

    def get_atestados_by_paciente(self, nome_paciente):
        """
        Busca atestados por nome do paciente em todas as consultas
        """
        atestados_do_paciente = []
        consultas = self.db.collection('consultas').stream()
        
        for consulta in consultas:
            atestados = self.db.collection('consultas').document(consulta.id).collection('atestados').where('paciente_nome', '==', nome_paciente).stream()
            for atestado in atestados:
                atestados_do_paciente.append(
                    Atestado(
                        paciente_nome=atestado.get('paciente_nome'),
                        cid=atestado.get('cid'),
                        dias_afastamento=atestado.get('dias_afastamento'),
                        data_inicio=atestado.get('data_inicio'),
                        id=atestado.id,
                        observacoes=atestado.get('observacoes')
                    )
                )
        return atestados_do_paciente

    def buscar_atestados_por_nome_parcial(self, nome_parcial):
        """
        Busca atestados por nome parcial do paciente
        Nota: Firestore não suporta busca parcial nativamente, então vamos buscar todos e filtrar
        """
        atestados_encontrados = []
        nome_busca = nome_parcial.lower()
        
        # Busca todos os atestados e filtra por nome
        todos_atestados = self.get_todos_atestados()
        
        for atestado in todos_atestados:
            if nome_busca in atestado.paciente_nome.lower():
                atestados_encontrados.append(atestado)
        
        return atestados_encontrados

    def update_atestado(self, consulta_id, atestado_id, paciente_nome, cid, dias_afastamento, data_inicio, observacoes=None):
        # Validar se atestado_id é um UUID v4 válido
        try:
            uuid.UUID(atestado_id, version=4)
        except ValueError:
            return None
        
        doc_ref = self.db.collection('consultas').document(consulta_id).collection('atestados').document(atestado_id)
        doc = doc_ref.get()
        
        if doc.exists:
            atestado = Atestado(
                paciente_nome=paciente_nome,
                cid=cid,
                dias_afastamento=dias_afastamento,
                data_inicio=data_inicio,
                id=atestado_id,
                observacoes=observacoes
            )
            doc_ref.set(atestado.to_dict())
            return atestado
        return None

    def delete_atestado(self, consulta_id, atestado_id):
        # Validar se atestado_id é um UUID v4 válido
        try:
            uuid.UUID(atestado_id, version=4)
        except ValueError:
            return False
        doc_ref = self.db.collection('consultas').document(consulta_id).collection('atestados').document(atestado_id)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False