# Desafio MBA Engenharia de Software com IA - Full Cycle

Ingestão de PDF em Postgres/pgVector e busca semântica por linha de comando, usando LangChain e Gemini.

## Pré-requisitos

- Python 3.12 ou 3.13 (3.14 ainda não tem wheels para parte das dependências no Windows)
- Docker
- Chave de API do Google AI Studio (Gemini)

## Configuração

```bash
cp .env.example .env
```

Preencher pelo menos `GOOGLE_API_KEY`. Os outros valores já vêm coerentes com o `docker-compose.yml`.

```bash
python3 -m venv venv
source venv/bin/activate            # Linux/macOS
# .\venv\Scripts\Activate.ps1       # Windows (PowerShell)
pip install -r requirements.txt
```

## Execução

```bash
docker compose up -d
python src/ingest.py
python src/chat.py
```

## Exemplo

```
PERGUNTA: Qual o faturamento da Empresa SuperTechIABrazil?
RESPOSTA: O faturamento foi de 10 milhões de reais.

PERGUNTA: Quantos clientes temos em 2024?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
```

Digite `sair` para encerrar.
