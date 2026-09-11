# Contrato de Dados — "Promessa ou Contradição?"

**Versão:** v0 · **Mantido por:** DE-3 (André Voigt, Arthur Sean) · **Última atualização:** 11/09/2026

Este documento define o formato que cada dataset do projeto precisa seguir.
Se você produz dados consumidos por outra equipe, eles precisam chegar neste formato.

---

## 1. Princípios


1) **IDs estáveis e legíveis**:

2) **Bronze imutável**:

3) **Mock nunca em data/silver/**:

Para cada uma: o que acontece se for violada?

---

## 2. Modelo de entidades


- Cardinalidade de cada relação e a chave que a materializa.


### Cadeia de lineage

```
proposal_id → chunk_id → document_id → page → source_url
```


---

## 3. Convenção de IDs

| Entidade | Padrão | Exemplo |
|---|---|---|
| Documento | `{CARGO}_{NNN}` | `PRES_001` |
| Chunk | `{document_id}_p{PPP}_c{CCC}` | `PRES_001_p014_c003` |


---

## 4. `data/bronze/metadata/documents.csv` — manifest

**Produzido por:** DE-1 · **Consumido por:** DE-2, DE-3

| Campo | Tipo | Obrigatório | Regra de validação | Exemplo |
|---|---|---|---|---|
| `document_id` | string | sim | | |
| `candidate` | string | sim | | |
| `party` | string | sim | | |
| `office` | enum | sim | | |
| `state` | string | sim | | |
| `source_url` | string | sim | | |
| `original_filename` | string | sim | | |
| `filename` | string | sim | | |
| `download_timestamp` | date (UTC) | sim | | |
| `dataset_version` | string | sim | | |
| `status` | enum | sim | | |


---

## 5. `data/silver/chunks.parquet`

**Produzido por:** DE-2 · **Validado por:** DE-3 · **Consumido por:** extração, RAG, evaluation

| Campo | Tipo | Obrigatório | Regra de validação | Exemplo |
|---|---|---|---|---|
| `chunk_id` | string | sim | | |
| `document_id` | string | sim | | |
| `page` | int | sim | | |
| `section` | string \| null | não | | |
| `text` | string | sim | | |
| `n_chars` | int | sim | | |
| `dataset_version` | string | sim | | |

---

## 6. `proposals` — formato futuro

**Produzido por:** equipe de extração · **Formato definido por:** DE-3


| Campo | Tipo | Obrigatório | Regra de validação | Exemplo |
|---|---|---|---|---|
| `proposal_id` | string | sim | | |
| `chunk_id` | string | sim | | |
| | | | | |

---

## 7. Entidade `Candidate`


---

## 8. Conjuntos permitidos

| Campo | Valores |
|---|---|
| `office` | `PRESIDENTE`, `GOVERNADOR` |
| `state` | UF (2 letras) ou `BR` |
| `status` | `ok`, `erro_download`, `arquivo_vazio`, `url_invalida` |


---

## 9. Como alterar este contrato

---

## 10. Changelog

| Versão | Data | Mudança |
|---|---|---|
| v0 | 11/09/2026 | Versão inicial, derivada da seção 3 do documento da Semana 1. |