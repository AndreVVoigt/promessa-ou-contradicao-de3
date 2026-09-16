import sys
from pathlib import Path
import pandas as pd
import pandera.pandas as pa
import pytest

BASE_DIR = Path(__file__).resolve().parents[2]
SCHEMA_DIR = BASE_DIR / "schema"
sys.path.append(str(SCHEMA_DIR))

from silver_schema import schema_silver

checagens = [
    "ID do chunk duplicado",
    "O ID não existe no manifest",
    "Página menor ou igual a zero",
    "Texto vazio",
]
def test_qualidade_dos_dados():
    df = pd.read_parquet("data/mock/silver_broken.parquet")

    try:
        schema_silver.validate(df, lazy=True)
    except pa.errors.SchemaErrors as err:
        checks_com_erro = set(err.failure_cases["check"].unique())
        linhas = []
        for check in checagens:
            if check in checks_com_erro:
                n = (err.failure_cases["check"] == check).sum()
                linhas.append(f"  FAILED - {check} ({n} ocorrência[s])")
            else:
                linhas.append(f"  PASS   - {check}")

        relatorio = "\n".join(linhas)
        pytest.fail(f"\n{relatorio}")