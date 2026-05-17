import json
from SPARQLWrapper import SPARQLWrapper, JSON

GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/biblioteca_temporal"

def exec_query(query):
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        print(f"Erro ao executar a query: {e}")
        return None
    
query = f"""
    PREFIX : <http://example.org/biblioteca-temporal#>
    select ?titulo ?tipoURI ?autor 
        ?evento ?nomEvento ?descricao
        where {{
        optional {{:Livro_Temporal_040 :titulo ?titulo .}}
        :Livro_Temporal_040 a ?tipoURI .   
        FILTER(?tipoURI in (:LivroHistorico, :LivroFiccional, :LivroParadoxal))
        :Livro_Temporal_040 :escritoPor/:nome ?autor .
        :Livro_Temporal_040 :existeEm ?linha .
        bind(STRAFTER(str(?linha), "#" )as ?linhaID)
        :Livro_Temporal_040 :refereEvento ?evento .
        ?evento :designacao ?nomEvento .
        ?evento :descricao ?descricao
    }}
    """

res = exec_query(query)

print(res["results"]["bindings"])

# # Extrair apenas os nomes dos livros e o nr de livros
# lista = []
# for livro in res["results"]["bindings"]:
#     lista.append(livro["livroID"]["value"].split("#")[-1]) 

# print(lista, len(lista))
