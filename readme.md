1. Clone o repositório
bashgit clone https://github.com/seu-usuario/flask-firestore-app.git
cd flask-firestore-app
2. Crie um ambiente virtual
bashpython -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
3. Instale as dependências
bashpip install -r requirements.txt
4. Configuração do Firebase

Acesse o Console do Firebase
Crie um novo projeto ou selecione um existente
Vá para Configurações do Projeto → Contas de serviço
Clique em Gerar nova chave privada
Baixe o arquivo JSON e renomeie para serviceAccountKey.json
Coloque o arquivo na raiz do projeto

5. Configuração das variáveis de ambiente
Crie um arquivo .env na raiz do projeto:
envFLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-super-segura
FIREBASE_CREDENTIALS=serviceAccountKey.json
PORT=5000
🚀 Como executar
Desenvolvimento
bashflask run
ou
bashpython app.py
A aplicação estará disponível em http://localhost:5000
