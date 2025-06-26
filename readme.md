1. Clone o repositório
git clone https://github.com/leonciods/Controle-consultas.git

2. Crie um ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

3. Instale as dependências
pip install -r requirements.txt

4. Configuração do Firebase
Acesse o Console do Firebase
Crie um novo projeto ou selecione um existente
Vá para Configurações do Projeto → Contas de serviço
Clique em Gerar nova chave privada
Baixe o arquivo JSON e renomeie para serviceAccountKey.json
Coloque o arquivo na raiz do projeto

5. Configuração das variáveis de ambiente
Crie um arquivo .env na raiz do projeto:
env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=sua-chave-secreta-super-segura
FIREBASE_CREDENTIALS=serviceAccountKey.json
PORT=5000

Como executar
Desenvolvimento
bash
flask run
ou
bash
python app.py
A aplicação estará disponível em http://localhost:5000
