# DE-3 · Modeling, Quality & Storage

Repositório da dupla DE-3 do projeto **"Promessa ou Contradição?"** — LED / CIn-UFPE.

- **Dupla:** André Voigt · Arthur Sean
## Estrutura

```
data/
├── mock/              # versionado — mocks que seguem o contrato
├── bronze/metadata/   # recebe documents.csv (DE-1) — não versionado
└── silver/            # recebe chunks.parquet (DE-2) — não versionado
src/quality/           # checks executáveis
schemas/               # schemas dos datasets em JSON Schema
docs/
├── data_contracts.md  # contrato oficial
notebooks/             # storage_poc.ipynb — validação, DuckDB e lineage
tests/                 # testes dos checks (positivos e negativos)
```



## Setup

```bash
git clone https://github.com/AndreVVoigt/promessa-ou-contradicao-de3.git
cd promessa-ou-contradicao-de3

python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
source .venv/bin/activate         # Linux 

pip install -r requirements.txt
```

Verificação rápida:

```bash
python -c "import pandas, pyarrow, duckdb, pytest; print('ok')"
```

## Como rodar a validação

**Testes dos checks** — confirma que cada check passa no mock válido e acusa a violação plantada no mock quebrado:

```bash
python -m pytest tests/ -v
```

**Demonstração completa** — relatório de qualidade, storage em DuckDB e lineage:

```
notebooks/storage_poc.ipynb
```

Abra o notebook e rode todas as células. Selecione o kernel do `.venv` (no VS Code: *Select Kernel → Python Environments → venv*), senão os imports de `src.quality` falham.


## Checks implementados

| Check | Dataset |
|---|---|
| `chunk_id` não nulo e único | chunks |
| `document_id` existe no manifest | chunks + manifest |
| `page >= 1` | chunks |
| `text` não vazio após strip | chunks |
| `office` e `state` em valores permitidos | manifest |