# Hospital Price Automation

Automação da atualização mensal de preços de medicamentos a partir das revistas **Brasíndice** (site) e **SIMPRO** (aplicativo desktop Delphi), com carga no SQL Server via stored procedures existentes.

## Requisitos

- Windows 11
- Python 3.11+ (com pip e no PATH)
- SQL Server acessível na rede
- Conta com acesso ao site Brasíndice e ao aplicativo SIMPRO

## Instalação

1. Instale o Python em https://www.python.org/downloads/ (marque "Add Python to PATH")
2. Crie e ative um ambiente virtual (opcional, recomendado):

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:

   ```powershell
   copy .env.example .env
   notepad .env
   ```

5. Ajuste `config/settings.json` com URLs, caminhos do aplicativo SIMPRO e nomes das stored procedures.

## Estrutura

```
hospital-price-automation/
├── .env.example              # Modelo de variáveis de ambiente (sem segredos)
├── .gitignore
├── requirements.txt
├── README.md
├── config/
│   └── settings.json         # URLs, caminhos e nomes de SPs
├── data/
│   ├── raw/                  # Arquivos gerados pelas revistas (não versionados)
│   └── processed/            # Arquivos normalizados (não versionados)
├── logs/                     # Logs de execução (não versionados)
├── src/
│   ├── brasicinde/           # Automação do site Brasíndice (Playwright)
│   │   └── automation.py
│   ├── simpro/               # Automação do desktop SIMPRO Delphi (pywinauto)
│   │   └── automation.py
│   ├── database/             # Conexão SQL Server e execução de SPs
│   │   ├── connection.py
│   │   └── scripts.py
│   └── utils/
│       └── logging.py
├── tests/
│   ├── brasicinde/
│   └── simpro/
└── workflows/
    └── monthly_update.py     # Orquestrador do fluxo mensal
```

## Fluxo

1. **Brasíndice**: Playwright acessa o site e executa a sequência fixa de cliques, salvando o arquivo em `data/raw/`.
2. **SIMPRO**: pywinauto abre o executável Delphi e executa a sequência fixa de cliques, salvando o arquivo em `data/raw/`.
3. **Banco**: `workflows/monthly_update.py` executa as duas stored procedures SQL Server já existentes, uma por revista.

## Segurança

- Credenciais só em `.env` (arquivo ignorado pelo Git) — nunca no código.
- Este projeto **não** armazena senhas em texto claro no repositório.

## Status

Estrutura inicial pronta. Os módulos de automação, conexão e orquestrador contêm apenas docstrings/esqueleto e serão implementados na próxima etapa.
