import sys
from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, POST

# Endpoints:
# O endpoint do SELECT/CONSTRUCT é o URL do repo
# O endpoint de UPDATE termina em /statements

REPO_URL = "http://localhost:7200/repositories/Mapa"
UPDATE_URL = f"{REPO_URL}/statements"

def expand_ontology(construct_query):
    sparql_read = SPARQLWrapper(REPO_URL)
    sparql_read.setQuery(construct_query)
    sparql_read.setReturnFormat(JSON)

    try:
        results = sparql_read.query().convert()
        triples = results.get   ("results", {}).get("bindings", [])
        if triples:
            insert_triples = ""
            for t in triples:
                if t['subject']['type'] == 'uri' :
                    s = f"<{t['subject']['value']}>"
                else:
                    s = f"'{t['subject']['value']}'"
                
                p = f"<{t['predicate']['value']}>"
                
                if t['object']['type'] == 'uri' :
                    o = f"<{t['object']['value']}>"
                else:
                    o = f"'{t['object']['value']}'"
                    if 'datatype' in t['object']:
                        o += f"^^<{t['object']['datatype']}>"

                insert_triples += f"{s} {p} {o} .\n"

            sparql_update = SPARQLWrapper(UPDATE_URL)
            sparql_update.setMethod(POST)

            insert_update = f"INSERT DATA {{ {insert_triples} }}"
            sparql_update.query()
            print(f"A inserir {len(triples)} triplos no repositorio...")
            sparql_update.query()
            print("Expansão concluída com sucesso!")
        else:
            print("A query não gerou novos triplos...")
    except Exception as e:
        print(f"Erro durante a operação: {e}")

if __name__ == "__main__":
    myQuery = """
PREFIX : <http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/>
construct {
    ?cidadeOrigem :ligadaA ?cidadeDestino . 
}
where {
    ?cidadeOrigem a :Cidade  . 
    ?l a :Ligacao ;
        :temOrigem ?cidadeOrigem;
        :temDestino ?cidadeDestino . 
} 
"""
    expand_ontology(myQuery)    


