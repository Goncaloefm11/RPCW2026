import json
import urllib.parse, re
from rdflib import Graph, Namespace, RDF, OWL

# 1. Carregar os dados JSON
data = """
[
  {
    "Indivíduo": "Abilio da Silva Ramalho",
    "Pai": "Manuel da Silva Ramalho 1866",
    "Mãe": "Custodia Azevedo 1867"
  },
  {
    "Indivíduo": "Albina Esteves de Araujo 1910",
    "Pai": "Henrique Luiz de Araujo 1867",
    "Mãe": "Maria Araujo 1884"
  },
  {
    "Indivíduo": "Ana da Silva Ramalho",
    "Pai": "Manuel da Silva Ramalho 1866",
    "Mãe": "Custodia Azevedo 1867"
  },
  {
    "Indivíduo": "Ana Margarida Ribeiro Leite 1980",
    "Pai": "Rui Alberto Araujo Leite 1948",
    "Mãe": "Maria Margarida Ribeiro 1954"
  },
  {
    "Indivíduo": "Antonio da Silva Ramalho 1904",
    "Pai": "Manuel da Silva Ramalho 1866",
    "Mãe": "Custodia Azevedo 1867"
  },
  {
    "Indivíduo": "Arminda da Silva Ramalho",
    "Pai": "Manuel da Silva Ramalho 1866",
    "Mãe": "Custodia Azevedo 1867"
  },
  {
    "Indivíduo": "Custodia Azevedo 1867",
    "Pai": "Jose Francisco Ramos Mouco",
    "Mãe": "Maria Gonçalves de Azevedo"
  },
  {
    "Indivíduo": "Domingos Couto Leite",
    "Pai": "Marçal da Costa Leite",
    "Mãe": "Flora Castilho do Couto Leite"
  },
  {
    "Indivíduo": "Emília Esteves de Araujo 1908",
    "Pai": "Henrique Luiz de Araujo 1867",
    "Mãe": "Maria Araujo 1884"
  },
  {
    "Indivíduo": "Ezequiel da Silva Ramalho",
    "Pai": "Manuel da Silva Ramalho 1866",
    "Mãe": "Custodia Azevedo 1867"
  },
  {
    "Indivíduo": "Filomena Esteves de Araujo 1927",
    "Pai": "Henrique Luiz de Araujo 1867",
    "Mãe": "Maria Araujo 1884"
  },
  {
    "Indivíduo": "Florinda Alves dos Santos",
    "Pai": "Joze da Silva Santos 1879",
    "Mãe": "Christina Rosa Silva Santos 1879"
  },
  {
    "Indivíduo": "Generosa da Silva Ramalho",
    "Pai": "Manuel da Silva Ramalho 1866",
    "Mãe": "Custodia Azevedo 1867"
  },
  {
    "Indivíduo": "Gilberto Couto Leite",
    "Pai": "Marçal da Costa Leite",
    "Mãe": "Flora Castilho do Couto Leite"
  },
  {
    "Indivíduo": "Helena Couto Leite",
    "Pai": "Marçal da Costa Leite",
    "Mãe": "Flora Castilho do Couto Leite"
  },
  {
    "Indivíduo": "Henrique Luís Esteves de Araujo 1924",
    "Pai": "Henrique Luiz de Araujo 1867",
    "Mãe": "Maria Araujo 1884"
  },
  {
    "Indivíduo": "Henrique Luiz de Araujo 1867",
    "Pai": "Jose Emílio de Araujo",
    "Mãe": "Maria das Dores Fernandes de Brito"
  },
  {
    "Indivíduo": "Henrique Marçal Araujo Leite 1943",
    "Pai": "Marçal Aristides Costa Leite 1909",
    "Mãe": "Maria Esteves de Araujo 1912"
  },
  {
    "Indivíduo": "Henrique Miguel Cabrita de Araujo Leite 1971",
    "Pai": "Henrique Marçal Araujo Leite 1943",
    "Mãe": "Maria Otília Araujo Leite 1944"
  },
  {
    "Indivíduo": "Ilda dos Santos Ramalho 1949",
    "Pai": "Antonio da Silva Ramalho 1904",
    "Mãe": "Maria Alves dos Santos 1906"
  },
  {
    "Indivíduo": "Isabel Maria Cabrita de Araujo Leite 1971",
    "Pai": "Henrique Marçal Araujo Leite 1943",
    "Mãe": "Maria Otília Araujo Leite 1944"
  },
  {
    "Indivíduo": "João Bernardo Couto Leite 1916",
    "Pai": "Marçal da Costa Leite",
    "Mãe": "Flora Castilho do Couto Leite"
  },
  {
    "Indivíduo": "Jose Carlos Leite Ramalho 1967",
    "Pai": "Jose dos Santos Ramalho 1942",
    "Mãe": "Maria Flora Araujo Leite 1941"
  },
  {
    "Indivíduo": "Jose dos Santos Ramalho 1942",
    "Pai": "Antonio da Silva Ramalho 1904",
    "Mãe": "Maria Alves dos Santos 1906"
  },
  {
    "Indivíduo": "Jose Emílio Esteves de Araujo 1916",
    "Pai": "Henrique Luiz de Araujo 1867",
    "Mãe": "Maria Araujo 1884"
  },
  {
    "Indivíduo": "Luís Esteves de Araujo 1918",
    "Pai": "Henrique Luiz de Araujo 1867",
    "Mãe": "Maria Araujo 1884"
  },
  {
    "Indivíduo": "Manuel Carlos dos Santos Ramalho",
    "Pai": "Antonio da Silva Ramalho 1904",
    "Mãe": "Maria Alves dos Santos 1906"
  },
  {
    "Indivíduo": "Manuel da Silva Ramalho 1866",
    "Pai": "Antonio da Silva Ramalho",
    "Mãe": "Maria Dias dos Reis"
  },
  {
    "Indivíduo": "Manuel Fernando dos Santos Ramalho",
    "Pai": "Antonio da Silva Ramalho 1904",
    "Mãe": "Maria Alves dos Santos 1906"
  },
  {
    "Indivíduo": "Marçal Aristides Costa Leite 1909",
    "Pai": "Marçal da Costa Leite",
    "Mãe": "Flora Castilho do Couto Leite"
  },
  {
    "Indivíduo": "Maria Alves dos Santos 1906",
    "Pai": "Joze da Silva Santos 1879",
    "Mãe": "Christina Rosa Silva Santos 1879"
  },
  {
    "Indivíduo": "Maria Araujo 1884",
    "Pai": "Jose Maria Esteves",
    "Mãe": "Emília Esteves"
  },
  {
    "Indivíduo": "Maria Esteves de Araujo 1912",
    "Pai": "Henrique Luiz de Araujo 1867",
    "Mãe": "Maria Araujo 1884"
  },
  {
    "Indivíduo": "Maria Flora Araujo Leite 1941",
    "Pai": "Marçal Aristides Costa Leite 1909",
    "Mãe": "Maria Esteves de Araujo 1912"
  },
  {
    "Indivíduo": "Maria Flora dos Santos Ramalho",
    "Pai": "Antonio da Silva Ramalho 1904",
    "Mãe": "Maria Alves dos Santos 1906"
  },
  {
    "Indivíduo": "Maria Helena Leite Ramalho 1968",
    "Pai": "José dos Santos Ramalho 1942",
    "Mãe": "Maria Flora Araujo Leite 1941"
  },
  {
    "Indivíduo": "Orlando Couto Leite",
    "Pai": "Marçal da Costa Leite",
    "Mãe": "Flora Castilho do Couto Leite"
  },
  {
    "Indivíduo": "Rosa Couto Leite",
    "Pai": "Marçal da Costa Leite",
    "Mãe": "Flora Castilho do Couto Leite"
  },
  {
    "Indivíduo": "Rui Alberto Araujo Leite 1948",
    "Pai": "Marçal Aristides Costa Leite 1909",
    "Mãe": "Maria Esteves de Araujo 1912"
  },
  {
    "Indivíduo": "Sara Esteves de Araujo 1914",
    "Pai": "Henrique Luiz de Araujo 1867",
    "Mãe": "Maria Araujo 1884"
  },
  {
    "Indivíduo": "Teresa Maria Ribeiro Leite 1985",
    "Pai": "Rui Alberto Araujo Leite 1948",
    "Mãe": "Maria Margarida Ribeiro 1954"
  },
  {
    "Indivíduo": "Virginia Esteves de Araujo 1921",
    "Pai": "Henrique Luiz de Araujo 1867",
    "Mãe": "Maria Araujo 1884"
  }
]
"""


# Carregar os dados garantindo que o Python trata o texto como UTF-8
registos = json.loads(data)

# 2. Configurar o Grafo e Namespaces
g = Graph()
# Base URI extraída do teu ficheiro familia.ttl
base_uri = "http://www.semanticweb.org/eduar_hkak6h8/ontologies/2026/3/untitled-ontology-4/"
NS = Namespace(base_uri)

g.bind("", NS)
g.bind("owl", OWL)

# Object Properties definidas na tua ontologia
temPai = NS.temPai
temMae = NS.temMae

def format_uri(name):
    # Substitui espaços por underscores para manter a legibilidade no Protégé
    # e codifica caracteres especiais de forma segura para URIs
    clean_name = re.sub(r'\s+', '_', name.strip())
    return NS[clean_name]

# 3. Povoar o grafo
for reg in registos:
    # Criar o indivíduo principal
    sujeito = format_uri(reg["Indivíduo"])
    g.add((sujeito, RDF.type, OWL.NamedIndividual))
    
    # Adicionar Pai
    if reg.get("Pai"):
        pai = format_uri(reg["Pai"])
        g.add((pai, RDF.type, OWL.NamedIndividual))
        g.add((sujeito, temPai, pai)) # Relação temPai
        
    # Adicionar Mãe
    if reg.get("Mãe"):
        mae = format_uri(reg["Mãe"])
        g.add((mae, RDF.type, OWL.NamedIndividual))
        g.add((sujeito, temMae, mae)) # Relação temMae

# 4. Exportar para Turtle com codificação UTF-8
g.serialize(destination="familia.ttl", format="turtle", encoding="utf-8")

print("Ficheiro 'familia_povoada.ttl' gerado com os acentos corrigidos!")