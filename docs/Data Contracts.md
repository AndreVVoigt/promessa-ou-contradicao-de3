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

```
Document
   ├── Page
   │     └── Chunk
   │            └── Proposal
   └── Candidate

```

| Relação | Cardinalidade | Chave que materializa |
|---|---|---|
| Document → Page | 1 : N | `Page.document_id` → `Document.document_id` |
| Page → Chunk | 1 : N | `(Chunk.document_id, Chunk.page)` → `(Page.document_id, Page.page)` |
| Chunk → Proposal | 1 : N | `Proposal.chunk_id` → `Chunk.chunk_id` |
| Document → Candidate | 1 : N | `Candidate.name` → `Document.candidate` |


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
| `document_id` | string | sim | Não nulo. Único no arquivo. Casa com `^PRES_\d{3}$`. | `PRES_001` |
| `candidate` | string | sim | Não nulo. Após `.strip()`, não vazio. Registra o nome como consta no plano de governo, sem normalização. | `Fulano de Tal` |
| `party` | string | sim | Não nulo. Após `.strip()`, não vazio. Sigla em maiúsculas, sem pontuação. | `XYZ` |
| `office` | enum | sim | Não nulo. Em {`PRESIDENTE`, `GOVERNADOR`}. Sensível a maiúsculas. No V0, sempre `PRESIDENTE`. | `PRESIDENTE` |
| `state` | string | sim | Não nulo. Duas letras maiúsculas (UF) ou `BR`. No V0, sempre `BR`. | `BR` |
| `source_url` | string | sim | Definir | Definir |
| `original_filename` | string | sim | Não nulo. Após `.strip()`, não vazio. Preserva o nome exato de origem, incluindo extensão. | `2026BR2800025\d{5}_01.pdf` |
| `filename` | string | sim | Não nulo. Após `.strip()`, não vazio. Único no arquivo. Sem espaços e sem acentos. Termina em `.pdf`. Se `status = ok`, o arquivo correspondente existe em `data/bronze/raw/`. | `PRES_001.pdf` |
| `download_timestamp` | date (UTC) | sim | Não nulo.  |  |
| `dataset_version` | string | sim | Não nulo. Casa com `^bronze_v\d+$`. Constante dentro de um mesmo arquivo. | `bronze_v0` |
| `status` | enum | sim | Não nulo. Em {`ok`, `erro_download`, `arquivo_vazio`, `url_invalida`}. Sensível a maiúsculas. | `ok` |
 
**Notas de validação**
 

- **`candidate` não é normalizado.** O nome é registrado como aparece no plano. Isso
  significa que o mesmo candidato pode aparecer com grafias diferentes se houver
  mais de um documento. Ver seção 7 para a consequência disso.
- **`original_filename` pode ter espaço, acento e parênteses; `filename` não.** A
  distinção é deliberada: o primeiro preserva a origem, o segundo é feito para ser usado em caminho de arquivo e em script sem quebrar.
---
 
## 5. `data/silver/chunks.parquet`
 
**Produzido por:** DE-2 · **Validado por:** DE-3 · **Consumido por:** extração, RAG, evaluation
 
| Campo | Tipo | Obrigatório | Regra de validação | Exemplo |
|---|---|---|---|---|
| `chunk_id` | string | sim | Não nulo. Único em todo o dataset. Casa com `^PRES_\d{3}_p\d{3}_c\d{3}$`. O trecho antes de `_p` é igual ao campo `document_id` da mesma linha. | `PRES_001_p014_c003` |
| `document_id` | string | sim | Não nulo. Existe na coluna `document_id` do manifest (integridade referencial). **Repete** — um documento tem muitos chunks. | `PRES_001` |
| `page` | int | sim | Não nulo. Inteiro ≥ 1. Igual ao `p\d{3}` do `chunk_id`. | `14` |
| `section` | string \| null | não | Definir | `Saúde` |
| `text` | string | sim | Não nulo. Após `.strip()`, não vazio. | `Ampliar o número de vagas em creches...` |
| `n_chars` | int | sim | Não nulo. Inteiro ≥ 1. Igual ao comprimento de `text`. | `47` |
| `dataset_version` | string | sim | Não nulo. Casa com `^silver_v\d+$`. Constante dentro de um mesmo arquivo. | `silver_v0` |
 
**Notas de validação**
 



---
 
## 6. `proposals` — formato futuro
 
**Produzido por:** equipe de extração estruturada · **Formato definido por:** DE-3
 
Ainda não existe. O formato abaixo é o mínimo necessário para que a cadeia de
lineage funcione; o restante será definido junto com a equipe de extração.
 
| Campo | Tipo | Obrigatório | Regra de validação | Exemplo |
|---|---|---|---|---|
| `proposal_id` | string | sim | Não nulo. Único em todo o dataset. Casa com `^PRES_\d{3}_p\d{3}_c\d{3}_r\d{2}$`. O trecho antes de `_r` é igual ao campo `chunk_id`. | `PRES_001_p014_c003_r01` |
| `chunk_id` | string | sim | Não nulo. Existe em `chunks.parquet` (integridade referencial). **Repete** — um chunk pode conter mais de uma proposta. | `PRES_001_p014_c003` |
| `text` | string | sim | Não nulo. Após `.strip()`, não vazio. Texto da proposta como extraída. | `Ampliar em 30% as vagas em creches` |
| `dataset_version` | string | sim | Não nulo. Casa com `^proposals_v\d+$`. | `proposals_v0` |
 
**Em aberto (decidir com a equipe de extração antes da primeira carga):**
 
- A proposta precisa guardar `page` e `document_id` próprios, ou basta subir a
  cadeia via `chunk_id`? Redundância facilita consulta, mas cria a possibilidade de
  os dois discordarem.
- Uma proposta pode atravessar dois chunks? Se sim, `chunk_id` único não basta e o
  modelo muda.
- Registrar o método de extração (regra, LLM, revisão humana) e a confiança? A
  equipe de Evaluation provavelmente vai precisar.
---
 
## 7. Entidade `Candidate`
 
<!-- Na V0, os dados do candidato ficam denormalizados no manifest, nos campos
`candidate` e `party`. Não há tabela própria nem `candidate_id`.
 
**Por que assim:** o corpus V0 tem um documento por candidato, e o objetivo da
semana é rastreabilidade do chunk até o PDF. Criar tabela de candidatos exigiria
decidir como tratar mudança de partido, nome de urna versus nome civil e
candidatura substituída — decisões que não bloqueiam nenhuma entrega da V0. Ver
`decisions.md`, D-02.
 
**O risco assumido:** como `candidate` registra o nome exatamente como aparece no
plano, o mesmo candidato pode surgir com grafias diferentes em documentos distintos
(`Fulano de Tal`, `FULANO DE TAL`, `Fulano Tal`). Agrupar por nome produziria
resultado errado sem avisar.
 
**Regra operacional que decorre disso:** toda agregação e todo join por candidato
usa `document_id`, nunca o campo `candidate`. O `document_id` é a identidade; o nome
é apenas rótulo de exibição.
 
**Revisar quando:** o corpus passar a ter mais de um documento por candidato, ou
quando for necessário comparar o mesmo candidato entre eleições. Aí a tabela
própria deixa de ser dívida e vira requisito. -->
 
---
 
## 8. Conjuntos permitidos
 
| Campo | Valores | Onde aparece |
|---|---|---|
| `office` | `PRESIDENTE`, `GOVERNADOR` | manifest |
| `state` | UF (2 letras maiúsculas) ou `BR` | manifest |
| `status` | `ok`, `erro_download`, `arquivo_vazio`, `url_invalida` | manifest |
 

---
 
## 9. Como alterar este contrato
<!-- 
1. **Avise antes, não depois.** Quem quer mudar um campo propõe a mudança no grupo e
   espera manifestação de quem produz e de quem consome aquele dataset. O custo de
   alinhar agora é de minutos; o de descobrir na integração é de dias.
2. **Incremente `dataset_version`.** Toda mudança que altera o formato produz uma
   versão nova (`silver_v0` → `silver_v1`). Datasets de versões diferentes não se
   misturam no mesmo arquivo.
3. **Atualize os mocks junto.** Os mocks em `data/mock/` são a expressão executável
   deste documento. Contrato alterado com mock velho significa que a suíte continua
   validando as regras antigas e passando.
4. **Registre no changelog**, com data e motivo.
**Por que mudança silenciosa é o pior caso:** se uma dupla acrescenta uma restrição
sem avisar, o mock da outra continua passando nos checks antigos. As duas partes
acreditam estar em conformidade, e a divergência só aparece quando os dados reais se
encontram — no pior momento possível. Um contrato que muda sem aviso é pior que não
ter contrato, porque produz falsa confiança.
 -->
---
 
## 10. Changelog
 
| Versão | Data | Mudança |
|---|---|---|
| v0 | 11/09/2026 | Versão inicial, derivada da seção 3 do documento da Semana 1. |