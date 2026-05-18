# Exame de Época Normal — RPCW 2026

## Identificação do Aluno
* **Nome:** Gonçalo Emanuel Ferreira Magalhães
* **Número Mecanográfico:** PG61524
* **Unidade Curricular:** Representação e Processamento de Conhecimento na Web

---

## Descrição do Trabalho

O exame prático foca-se na modelação de ontologias em OWL, povoamento de dados e posterior consulta e enriquecimento de grafos via SPARQL, dividindo-se em duas partes:

1. **Exercício 1 (A Fábula):** Modelação da história do Mestre Corvo e da Mestre Raposa. Mapeia as classes de personagens, animais, sentimentos, localizações e as suas interações diretas (posse do queijo e o ato de enganar).
2. **Exercício 2 (Jogos de Tabuleiro Modernos):** Desenvolvimento de uma infraestrutura semântica escalável sob o IRI dinâmico exigido: `http://www.di.uminho.pt/rpcw2026/PG61524/`.

---

## Organização do Projeto

O repositório encontra-se estruturado com os seguintes ficheiros:

* `fabula.ttl` — Ontologia conceptual e população de indivíduos da fábula (Exercício 1).
* `queries.txt` — Ficheiro de texto contendo todas as consultas SPARQL desenvolvidas para o Exercício 1.
* `boardgames_base.ttl` — Vocabulário base contendo as classes, atributos e object properties construídas para o Exercício 2.
* `povoar_boardgames.py` — Script de automação em Python para o processamento e mapeamento inicial dos dados.
* `autores.json`, `editoras.json`, `jogos.json`, `mecanicas.json`, `premios.json` — Conjuntos de informação fornecidos que serviram como ponto de partida.
* `boardgames_ind.ttl` — Grafo de conhecimento povoado final **já maximizado**. *Nota: Este ficheiro foi exportado diretamente do GraphDB após a execução bem-sucedida das queries de mutação, contendo todas as relações inferidas de forma estática.*
* `sparql.txt` — Ficheiro de texto contendo as consultas analíticas, agregadas e de inferência desenvolvidas para o Exercício 2.

---

## Metodologia de Migração e Inferência (Exercício 2)

### Povoamento Inicial Automático
Para o processamento dos datasets JSON, utilizou-se o script Python (`povoar_boardgames.py`) suportado pela biblioteca `rdflib`. O script foi desenhado com uma função de segurança (`criar_no_seguro`) que valida se um recurso referenciado de forma cruzada (ex: um jogo associado a um prémio ou mecânica) já se encontra instanciado no grafo. Caso não exista, o indivíduo é criado automaticamente na sua classe correspondente, blindando a ontologia contra falhas de integridade referencial.

### Enriquecimento Semântico por Inferência
A instanciação das propriedades inversas pedidas no enunciado foi executada na base de dados gráfica através do motor SPARQL Update:
* **Relações Geradas:** `:isPublishedBy` (inversa de `:publishedGame`) e `:hasMechanic` (inversa de `:usedInGame`).
* **Mecanismo:** Foram aplicadas queries `INSERT` que analisaram as conexões existentes e geraram os caminhos lógicos inversos, maximizando o grafo final.

---

## Instruções de Execução e Replicação (Correção)

Para garantir o isolamento dos dados e evitar conflitos de prefixos, a validação das alíneas deve ser feita através de dois repositórios independentes no GraphDB:

### 1. Validação do Exercício 1 (A Fábula)
1. No GraphDB, crie um repositório chamado **`fabula`**.
2. Efetue o upload e o import do ficheiro **`fabula.ttl`**.
3. No painel **SPARQL**, execute as consultas presentes no ficheiro **`queries.txt`**.

### 2. Validação do Exercício 2 (Jogos de Tabuleiro)
1. No GraphDB, crie um repositório chamado **`boardgames`**.
2. Efetue o upload e o import do ficheiro base **`boardgames_base.ttl`**.
3. Efetue o upload e o import do ficheiro povoado final **`boardgames_ind.ttl`**.
4. No painel **SPARQL**, execute as consultas analíticas presentes no ficheiro **`sparql.txt`**.
5. *(Opcional)* As queries de mutação `INSERT` utilizadas para gerar as propriedades inversas encontram-se mapeadas na secção final do ficheiro **`sparql.txt`**.
