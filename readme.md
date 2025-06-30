## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta no Google Cloud Platform
- Projeto Firebase configurado

## ⚙️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/leonciods/Controle-consultas.git

```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configuração do Firebase

1. Acesse o [Console do Firebase](https://console.firebase.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Vá para **Configurações do Projeto** → **Contas de serviço**
4. Clique em **Gerar nova chave privada**
5. Baixe o arquivo JSON e renomeie para `serviceAccountKey.json`
6. Coloque o arquivo na raiz do projeto


## 🚀 Como executar

### Desenvolvimento
```bash
flask run
```
ou
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`
