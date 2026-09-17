import sys
from pathlib import Path
import pandas as pd
import pandera.pandas as pa
import pytest

BASE_DIR = Path(__file__).resolve().parents[2]
SCHEMA_DIR = BASE_DIR / "schema"
sys.path.append(str(SCHEMA_DIR))

from silver_schema import schema_silver
from documents_schema import schema_documents
checagens_silver = [
    "ID do chunk duplicado",
    "O ID não existe no manifest",
    "Página menor ou igual a zero",
    "Texto vazio",
]

checagens_documents = [
    "Candidato a presidência não deve constar uma UF estadual",
    "Candidato a governador deve constar uma UF estadual válida",
    "Cargo inválido",
    "UF inválida"
]
def test_qualidade_dos_dados_silver():
    df_silver = pd.read_parquet("data/mock/silver_broken.parquet")
    try:
        schema_silver.validate(df_silver, lazy=True)
    except pa.errors.SchemaErrors as err:
        checks_com_erro = set(err.failure_cases["check"].unique())
        linhas = []
        for check in checagens_silver:
            if check in checks_com_erro:
                n = (err.failure_cases["check"] == check).sum()
                linhas.append(f"  FAILED - {check} ({n} ocorrência[s])")
            else:
                linhas.append(f"  PASS   - {check}")

        relatorio = "\n".join(linhas)
        pytest.fail(f"\n{relatorio}", pytrace=False)

def test_qualidade_dos_dados_documents():
    df_documents = pd.read_csv("data/mock/documents_broken.csv")
    try:
        schema_documents.validate(df_documents, lazy=True)
    except pa.errors.SchemaErrors as err:
        checks_com_erro = set(err.failure_cases["check"].unique())
        linhas = []
        for check in checagens_documents:
            if check in checks_com_erro:
                n = (err.failure_cases["check"] == check).sum()
                linhas.append(f"  FAILED - {check} ({n} ocorrência[s])")
            else:
                linhas.append(f"  PASS   - {check}")

        relatorio = "\n".join(linhas)
        pytest.fail(f"\n{relatorio}", pytrace=False)


