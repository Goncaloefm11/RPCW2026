# TPC
- Fazer página detalhe livro
```python
@app.route('/livro/<id_livro>')
def rota_livro(id_livro)
    #info do livro
        # id, titulo, tipo, autor, país, linha temporal (pode ser mais que uma), eventos referidos pelo livro (id, nome, descrição)
```

- Fazer página Eventos
```python
@app.route('/eventos')
    def rota_eventos():
        # id, designação, descrição, lista de livros que referem o evento
``` 
Problema: quantas dimensoes tem a tabela. SParql 2 dimensoes, tpc 3 dimensoes
query usar GROUP_CONCAT
não obrigatorio fazer com GROUP_CONCAT

# Ex 1
1. Descarregar dataset
2. Criar repo no GraphDB: biblioteca_temporal
3. Query Sparql que recupere os ids dos livros:
- id de 1 livro: http://example.org/biblioteca_temporal#idLivro
- Extrair apenas `idLivro`
- STRAFTER(..., "#")


# Ex 2
```sparql
PREFIX : <http://example.org/biblioteca-temporal#>
select ?livroID where {
    ?livro a :Livro . 
    BIND(STRAFTER(STR((?livro)), "#") AS ?livroID)
} 
```

# EX 3 - Temos 113 livros. Extrair Titulo do livro.
```sparql
PREFIX : <http://example.org/biblioteca-temporal#>
select ?livroID ?titulo where {
    ?livro a :Livro . 
    optional {?livro :titulo ?titulo . } 
    BIND(STRAFTER(STR((?livro)), "#") AS ?livroID)
} 
```

# EX 4 - Extrair nome do Autor
Livro -> :escritoPor -> autor -> :nome -> nomeAutor

```sparql
PREFIX : <http://example.org/biblioteca-temporal#>
select ?livroID ?titulo ?nomeAutor where {
    ?livro a :Livro . 
    optional {?livro :titulo ?titulo . } 	
    ?livro :escritoPor/:nome ?nomeAutor .
    BIND(STRAFTER(STR((?livro)), "#") AS ?livroID)
} 
```

# EX 5 - Extrair país de origem
Livro -> :escritoPor -> autor -> :paisOrigem -> país
```sparql
PREFIX : <http://example.org/biblioteca-temporal#>
select ?livroID ?titulo ?nomeAutor ?país where {
    ?livro a :Livro . 
    optional {?livro :titulo ?titulo . } 	
    ?livro :escritoPor/:nome ?nomeAutor .
    ?livro :escritoPor/:paisOrigem ?país .
    BIND(STRAFTER(STR((?livro)), "#") AS ?livroID)
} 
```

# EX 6 - Extrair Tipo de Livro
```sparql
PREFIX : <http://example.org/biblioteca-temporal#>
select ?livroID ?titulo ?tipoLivro ?nomeAutor ?país where {
    ?livro a ?tipoLivro . 
    FILTER(?tipoLivro in (:LivroHistorico, :LivroFiccional,:LivroParadoxal))
    optional {?livro :titulo ?titulo . } 	
    ?livro :escritoPor/:nome ?nomeAutor .
    ?livro :escritoPor/:paisOrigem ?país .
    BIND(STRAFTER(STR((?livro)), "#") AS ?livroID)
} order by ?titulo
```

# EX 7 - BibApp
BibApp/app.py
BibApp/templates/jinja2

