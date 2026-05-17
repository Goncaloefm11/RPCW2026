import json

file = "mapa-virtual.json"

with open(file, 'r', encoding='utf-8') as f:
    dados = json.load(f)

# Cabeçalho

base_uri = "http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/"
ttl_conteudo = f""" 
@prefix : <http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/> .

<http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/pertenceADistrito
:pertenceADistrito rdf:type owl:ObjectProperty ;
                   owl:inverseOf :temCidade ;
                   rdfs:domain :Cidade ;
                   rdfs:range :Distrito .


###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/temCidade
:temCidade rdf:type owl:ObjectProperty .


###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/temDestino
:temDestino rdf:type owl:ObjectProperty ;
            rdfs:domain :Ligacao ;
            rdfs:range :Cidade .


###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/temOrigem
:temOrigem rdf:type owl:ObjectProperty ;
           rdfs:domain :Ligacao ;
           rdfs:range :Cidade .


#################################################################
#    Data properties
#################################################################

###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/temDescricao
:temDescricao rdf:type owl:DatatypeProperty ;
              rdfs:domain :Cidade ;
              rdfs:range xsd:string .


###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/temDistancia
:temDistancia rdf:type owl:DatatypeProperty ;
              rdfs:domain :Ligacao ;
              rdfs:range xsd:float .


###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/temId
:temId rdf:type owl:DatatypeProperty ;
       rdfs:domain [ rdf:type owl:Class ;
                     owl:unionOf ( :Cidade
                                   :Distrito
                                   :Ligacao
                                 )
                   ] ;
       rdfs:range xsd:string .


###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/temNome
:temNome rdf:type owl:DatatypeProperty ;
         rdfs:domain [ rdf:type owl:Class ;
                       owl:unionOf ( :Cidade
                                     :Distrito
                                   )
                     ] ;
         rdfs:range xsd:string .


###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/temPopulacao
:temPopulacao rdf:type owl:DatatypeProperty ;
              rdfs:domain :Cidade ;
              rdfs:range xsd:integer .


#################################################################
#    Classes
#################################################################

###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/Cidade
:Cidade rdf:type owl:Class .


###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/Distrito
:Distrito rdf:type owl:Class .


###  http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/mapa-virtual/Ligacao
:Ligacao rdf:type owl:Class .

#################################################################
#    Indivíduos
#################################################################

### Distritos

"""


# Povoar Distritos
distritos = set(c['distrito'] for c in dados['cidades'])

for d in distritos:
    d_id = d.replace(" ", "_").lower()
    ttl_conteudo += f"""
:d_{d_id} a :Distrito ;
    :temNome "{d}" .
    """

# Povoar Cidades
ttl_conteudo += "\n\n### Cidades\n"

for c in dados['cidades']:
    d_id = c['distrito'].replace(" ", "_").lower()
    desc = c['descrição'].replace('"', '\\"')  # Escapar aspas
    c_id = c['nome'].replace(" ", "_").lower()

    ttl_conteudo += f"""
:{c['id']} a :Cidade ;
    :temId "{c['id']}" ;
    :temNome "{c['nome']}" ;
    :temPopulacao {c['população']} ;
    :temDescricao "{desc}" ;
    :pertenceADistrito :d_{d_id} .
   """
    
# Povoar Ligações
ttl_conteudo += "\n\n### Ligações\n"

for l in dados['ligações']:
    ttl_conteudo += f"""
:{l['id']} a :Ligacao ;
:temId "{l['id']}" ;
:temDistancia "{l['distância']}"^^xsd:float ;
:temOrigem :{l['origem']} ;
:temDestino :{l['destino']} .
    """

# Escrever para o ficheiro .ttl
output= "mapa.ttl"
with open(output, 'w', encoding='utf-8') as f:
    f.write(base_uri + ttl_conteudo)

print(f"Sucesso: Ontologia gerada em '{output}' com {len(dados['cidades'])} cidades e {len(dados['ligações'])} ligações.")

