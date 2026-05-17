import json
import re
from rdflib import Graph, Namespace, URIRef, RDF, OWL

# 1. Configuração do Grafo e Namespaces
g = Graph()
NS = Namespace("http://www.semanticweb.org/gugafm11/ontologies/2026/untitled-ontology-23")
g.bind("", NS)

# 2. Função para normalizar nomes para URIs (substituir espaços por underscores)
def fix_uri(name):
    if not name:
        return None
    else:
        # Substitui espaços e caracteres especiais por underscores
        name_clean = re.sub(r'\s+', '_', name.strip())
        return NS[name_clean]

# 3. Carregar o ficheiro JSON
try:
    with open('familia.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Erro: O ficheiro 'familia.json' não foi encontrado.")
    data = []

# 4. Processar os dados e adicionar ao grafo
for item in data:
    sujeito_nome = item.get("Indivíduo")
    pai_nome = item.get("Pai")
    mae_nome = item.get("Mãe")

    if sujeito_nome:
        sujeito_uri = fix_uri(sujeito_nome)
        
        # Declarar o indivíduo como NamedIndividual
        g.add((sujeito_uri, RDF.type, OWL.NamedIndividual))
        
        # Adicionar relação de Pai
        if pai_nome:
            pai_uri = fix_uri(pai_nome)
            g.add((sujeito_uri, NS.temPai, pai_uri))
            g.add((pai_uri, RDF.type, OWL.NamedIndividual)) # Garante que o pai também é um indivíduo
            
        # Adicionar relação de Mãe
        if mae_nome:
            mae_uri = fix_uri(mae_nome)
            g.add((sujeito_uri, NS.temMae, mae_uri))
            g.add((mae_uri, RDF.type, OWL.NamedIndividual)) # Garante que a mãe também é um indivíduo

# 5. Serializar e guardar o resultado em TTL
output_file = "familia_gerada.ttl"
g.serialize(destination=output_file, format="turtle", encoding="utf-8")

print(f"Ontologia gerada com sucesso em: {output_file}")