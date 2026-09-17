import pandera.pandas as pa
import pandas as pd
df_documentos = pd.read_csv("data/mock/documents_mock.csv")

OFFICE = ("PRESIDENTE", "GOVERNADOR")
STATE_GOV = (
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
    "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
    "SP", "SE", "TO"
)
STATE_PRE = "BR"
STATE_TOT = STATE_GOV+ (STATE_PRE,)

schema_documents = pa.DataFrameSchema(
    columns={
    "document_id": pa.Column(str),
    "candidate": pa.Column(str),
    "party": pa.Column(str),
    "office": pa.Column(str, checks=pa.Check.isin(OFFICE, error="Cargo inválido")),
    "state": pa.Column(str, checks=pa.Check.isin(STATE_TOT, error="UF inválida")),
    "source_url": pa.Column(str),
    "original_filename": pa.Column(str),
    "filename": pa.Column(str),
    "download_timestamp": pa.Column(pa.DateTime, coerce=True),
    "dataset_version": pa.Column(str),
    "status": pa.Column(str)
}, checks=[
    pa.Check(lambda df: (df["office"] != "PRESIDENTE") | (df["state"] == STATE_PRE),error="Candidato a presidência não deve constar uma UF estadual"), 
    pa.Check(lambda df: (df["office"] != "GOVERNADOR") | (df["state"].isin(STATE_GOV)), error="Candidato a governador deve constar uma UF estadual válida")
],  strict=True, coerce=False)