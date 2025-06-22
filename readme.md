# Como Rodar o Projeto

Siga os passos abaixo para configurar e executar o projeto localmente.

## 1. Clone o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DA_PASTA>
```

## 2. Ambiente Python

### a) Crie um ambiente virtual

```bash
python -m venv venv
```

### b) Ative o ambiente virtual

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Linux/Mac:**
  ```bash
  source venv/bin/activate
  ```

### c) Instale as dependências Python

```bash
pip install -r requirements.txt
```
### d) Baixe o modelo no Ollama
```bash
ollama pull llama3.1
```

## 3. Ambiente Node.js

### a) Instale as dependências Node.js

```bash
npm install
```

## 4. Rodando o Projeto

- **Backend (Python):**
  ```bash
  python -m src.main 
  ```
- **Integração com Whatsapp (Node.js):**
  ```bash
  node bot.js
  ```

## 5. Observações

- Certifique-se de ter o Python e o Node.js instalados em sua máquina.
- É necessario scannear o QR Code do WhatsApp para autenticar o bot.
- O bot irá responder automaticamente às mensagens recebidas no WhatsApp.
