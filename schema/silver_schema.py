import pandera.pandas as pa
import pandas as pd
df_documentos = pd.read_csv("data/mock/documents_mock.csv")
schema_silver = pa.DataFrameSchema({
    "chunk_id": 
    pa.Column(str, checks=
              [pa.Check(lambda f: ~f.duplicated(), error="ID do chunk duplicado"),]),
    "document_id": 
    pa.Column(str, checks=[
              pa.Check(lambda f: f.isin(df_documentos["document_id"]), error="O ID não existe no manifest")]),
    "page": pa.Column(int, checks=
                      pa.Check.gt(0, error="Página menor ou igual a zero")),
    "section": pa.Column(str, nullable=True),
    "text": pa.Column(str, checks=pa.Check(lambda check_texto: check_texto.str.strip().str.len() > 0, error="Texto vazio")),
    "n_chars": pa.Column(int),
    "dataset_version": pa.Column(str)
}, strict=True, coerce=False)
