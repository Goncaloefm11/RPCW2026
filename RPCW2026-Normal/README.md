# Exame de Época Normal — RPCW 2026

## Identificação do Aluno
* **Nome:** Gonçalo Emanuel Ferreira Magalhães
* **Número Mecanográfico:** PG61524
* **Unidade Curricular:** Representação e Processamento de Conhecimento na Web

---

## Descrição do Trabalho

O exame prático divide-se em duas partes fundamentais, focadas na modelação de ontologias em OWL e na posterior consulta e enriquecimento de dados via SPARQL.

### Exercício 1: A Fábula
Modelação da história do Mestre Corvo e da Mestre Raposa. A ontologia estrutural foi construída e povoada diretamente em sintaxe Turtle no ficheiro `fabula.ttl`, mapeando as classes de personagens, animais, sentimentos, localizações e as suas interações (como o ato de enganar e a posse do queijo).

### Exercício 2: Jogos de Tabuleiro Modernos
Desenvolvimento de uma infraestrutura semântica escalável para o ecossistema de jogos de tabuleiro. O trabalho assentou no IRI dinâmico exigido no enunciado: `http://www.di.uminho.pt/rpcw2026/PG61524/`.

---

## Metodologia de Migração e Povoamento (Exercício 2)

O processo de povoamento dos indivíduos foi completamente automatizado através de um **script em Python**, garantindo a integridade referencial e a rapidez na transição dos dados fornecidos em formato JSON.

### O Script de Automação (`povoar_boardgames.py`)
O script utiliza a biblioteca `rdflib` e atua de acordo com o seguinte fluxo lógico:
1. **Carregamento Estrutural:** Lê e interpreta a ontologia esqueleto a partir do ficheiro `boardgames_base.ttl`.
2. **Parseamento de Datasets:** Processa sequencialmente os ficheiros JSON fornecidos: `jogos.json`, `autores.json`, `editoras.json`, `mecanicas.json` e `premios.json`.
3. **Resolução de Integridade Lógica:** Foi desenhado com uma função de segurança (`criar_no_seguro`) que valida se um recurso referenciado (ex: um jogo associado a uma mecânica ou prémio) já existe no grafo. Caso não exista no ficheiro principal, o indivíduo é instanciado automaticamente com a sua classe respetiva, prevenindo falhas de integridade referencial nas propriedades de objeto.
4. **Serialização:** Exporta o grafo consolidado em formato Turtle para o ficheiro `boardgames_ind.ttl`.

---

## Inferência de Novo Conhecimento

A instanciação das propriedades inversas pedidas foi executada diretamente na base de dados gráfica, tirando partido do motor de inferência SPARQL:
* **Relações Geradas:** `:isPublishedBy` (inversa de `:publishedGame`) e `:hasMechanic` (inversa de `:usedInGame`).
* **Execução:** Foram aplicadas as queries de mutação `INSERT` na interface do GraphDB para interligar os dados de forma permanente e bidirecional na ontologia.

---

## Instruções de Execução e Replicação (Correção)

Para garantir que não ocorre mistura de dados ou conflitos de prefixos entre os dois domínios independentes do exame, a validação deve ser feita criando dois repositórios separados no GraphDB:

### 1. Testar o Exercício 1 (A Fábula)
1. No GraphDB, crie um repositório separado chamado **`fabula`**.
2. Efetue o upload e o import do ficheiro **`fabula.ttl`**.
3. Navegue até ao painel **SPARQL**, garanta que o repositório `fabula` está selecionado e execute as quatro primeiras queries (as referentes à Fábula) presentes no ficheiro `queries.txt`.

### 2. Testar o Exercício 2 (Jogos de Tabuleiro)
1. No GraphDB, crie um novo repositório chamado **`boardgames`**.
2. Efetue o upload e o import do ficheiro de axiomas base **`boardgames_base.ttl`**.
3. Efetue o upload e o import do ficheiro povoado final **`boardgames_ind.ttl`**.
4. No painel **SPARQL** (com o repositório `boardgames` ativo), execute as queries analíticas e as de agregação listadas no ficheiro `sparql.txt`.
5. Para materializar o conhecimento e as relações inversas, execute as queries `INSERT` presentes na secção final do ficheiro `sparql.txt`.