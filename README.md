# DE-3 · Modeling, Quality & Storage

> **Contrato de dados oficial do projeto.** DE-1 e DE-2: o formato que os
> datasets precisam seguir está em [`docs/data_contracts.md`](docs/data_contracts.md).
> Mudanças no contrato são avisadas no grupo antes de valerem.

Repositório da dupla DE-3 do projeto **"Promessa ou Contradição?"** — LED / CIn-UFPE.

- **Dupla:** André Voigt · Arthur Sean




## Estrutura

```
data/
├── mock/              # versionado — mocks que seguem o contrato
├── bronze/metadata/   # recebe documents.csv (DE-1) — não versionado
└── silver/            # recebe chunks.parquet (DE-2) — não versionado
src/quality/           # checks executáveis
schemas/               # schemas das entidades
docs/
├── data_contracts.md  # contrato oficial
└── decisions.md       # decisões tomadas e dúvidas abertas
notebooks/             
tests/                 # testes dos checks (positivos e negativos)
```

`data/mock/` vai para o git de propósito: é o que permite desenvolver e testar
antes do dado real existir, e é a prova de que o contrato está bem definido.
As camadas Bronze e Silver nunca são versionadas.

## Setup

```bash
git clone <https://github.com/AndreVVoigt/promessa-ou-contradicao-de3.git>
cd <pasta>

python3 -m venv .venv
.venv\Scripts\Activate.ps1        # Linux source .venv/bin/activate       

pip install -r requirements.txt
```

Verificação rápida:

```bash
python -c "import pandas, pyarrow, duckdb, pandera, pytest; print('ok')"
```
