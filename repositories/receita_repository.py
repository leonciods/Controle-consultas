from firestore.firebase_config import init_firebase
from models.receita import Receita
import uuid

class ReceitaRepository:
    def __init__(self):
        self.db = init_firebase()

    def add_receita(self, consulta_id, receita):
        # Usar o ID UUID v4 gerado pela classe Receita
        collection = self.db.collection('consultas').document(consulta_id).collection('receitas')
        doc_ref = collection.document(receita.id)
        doc_ref.set(receita.to_dict())
        return receita

    def get_all_receitas(self, consulta_id):
        collection = self.db.collection('consultas').document(consulta_id).collection('receitas')
        return [
            Receita(
                medicamento=doc.get('medicamento'),
                dosagem=doc.get('dosagem'),
                paciente_nome=doc.get('paciente_nome'),
                id=doc.id,
                observacoes=doc.get('observacoes'),
                duracao=doc.get('duracao')
            ) for doc in collection.stream()
        ]

    def get_receita_by_id(self, consulta_id, receita_id):
        # Validar se receita_id é um UUID v4 válido
        try:
            uuid.UUID(receita_id, version=4)
        except ValueError:
            return None
        doc = self.db.collection('consultas').document(consulta_id).collection('receitas').document(receita_id).get()
        if doc.exists:
            return Receita(
                medicamento=doc.get('medicamento'),
                dosagem=doc.get('dosagem'),
                paciente_nome=doc.get('paciente_nome'),
                id=doc.id,
                observacoes=doc.get('observacoes'),
                duracao=doc.get('duracao')
            )
        return None

    def get_todas_receitas(self):
        # Busca todas as receitas de todas as consultas (para farmácia)
        todas_receitas = []
        consultas = self.db.collection('consultas').stream()
        
        for consulta in consultas:
            receitas = self.db.collection('consultas').document(consulta.id).collection('receitas').stream()
            for receita in receitas:
                todas_receitas.append(
                    Receita(
                        medicamento=receita.get('medicamento'),
                        dosagem=receita.get('dosagem'),
                        paciente_nome=receita.get('paciente_nome'),
                        id=receita.id,
                        observacoes=receita.get('observacoes'),
                        duracao=receita.get('duracao')
                    )
                )
        return todas_receitas

    def get_receitas_by_paciente(self, nome_paciente):
        """
        Busca receitas por nome do paciente em todas as consultas
        """
        receitas_do_paciente = []
        consultas = self.db.collection('consultas').stream()
        
        for consulta in consultas:
            receitas = self.db.collection('consultas').document(consulta.id).collection('receitas').where('paciente_nome', '==', nome_paciente).stream()
            for receita in receitas:
                receitas_do_paciente.append(
                    Receita(
                        medicamento=receita.get('medicamento'),
                        dosagem=receita.get('dosagem'),
                        paciente_nome=receita.get('paciente_nome'),
                        id=receita.id,
                        observacoes=receita.get('observacoes'),
                        duracao=receita.get('duracao')
                    )
                )
        return receitas_do_paciente

    def buscar_receitas_por_nome_parcial(self, nome_parcial):
        """
        Busca receitas por nome parcial do paciente
        Nota: Firestore não suporta busca parcial nativamente, então vamos buscar todas e filtrar
        """
        receitas_encontradas = []
        nome_busca = nome_parcial.lower()
        
        # Busca todas as receitas e filtra por nome
        todas_receitas = self.get_todas_receitas()
        
        for receita in todas_receitas:
            if nome_busca in receita.paciente_nome.lower():
                receitas_encontradas.append(receita)
        
        return receitas_encontradas

    def update_receita(self, consulta_id, receita_id, medicamento, dosagem, observacoes=None, duracao=None):
        # Validar se receita_id é um UUID v4 válido
        try:
            uuid.UUID(receita_id, version=4)
        except ValueError:
            return None
        
        doc_ref = self.db.collection('consultas').document(consulta_id).collection('receitas').document(receita_id)
        doc = doc_ref.get()
        
        if doc.exists:
            # Manter o nome do paciente original
            paciente_nome = doc.get('paciente_nome')
            receita = Receita(
                medicamento=medicamento,
                dosagem=dosagem,
                paciente_nome=paciente_nome,
                id=receita_id,
                observacoes=observacoes,
                duracao=duracao
            )
            doc_ref.set(receita.to_dict())
            return receita
        return None

    def delete_receita(self, consulta_id, receita_id):
        # Validar se receita_id é um UUID v4 válido
        try:
            uuid.UUID(receita_id, version=4)
        except ValueError:
            return False
        doc_ref = self.db.collection('consultas').document(consulta_id).collection('receitas').document(receita_id)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False