import json
from rdflib import Graph, Namespace, RDF, OWL, Literal, XSD

# Carregar a ontologia base
g = Graph()
g.parse("Entre_Hoje_e_Amanha.ttl", format="turtle")

# O namespace deve ser o IRI que vês no Protegé (terminado em #)
BT = Namespace("http://www.semanticweb.org/gugafm11/ontologies/2026/untitled-ontology-15#")

# Garante que associas o prefixo vazio a este namespace no grafo
g.bind("", BT)

# Mapeamento: tipo no JSON → classe na ontologia
CLASSES = {
    "LinhaOriginal": BT.LinhaOriginal,
    "LinhaAlternativa": BT.LinhaAlternativa,
    "Biblioteca": BT.Biblioteca,
    "EventoHistorico": BT.EventoHistorico,
    "EventoFuturo": BT.EventoFuturo,
    "Bibliotecario": BT.Bibliotecario,
    "Autor": BT.Autor,
    "Leitor": BT.Leitor,
    "LivroHistorico": BT.LivroHistorico,
    "LivroFiccional": BT.LivroFiccional,
    "LivroParadoxal": BT.LivroParadoxal,
    "Livro": BT.Livro,
}

# Mapeamento: chave no JSON → object property na ontologia
PROPS = {
    "escritoPor": BT.saoEscritosPor,
    "pertenceA": BT.pertecemA,       # nota: typo original na ontologia
    "existeEm": BT.existemEm,
    "refereEvento": BT.refereEvento,
    "trabalhaEm": BT.trabalhamEm,
    "requisitam": BT.requisitam,
}

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def add_individuals(data):
    for item in data:
        uri = BT[item["id"]]

        # Tipo (classe)
        tipo = item.get("tipo")
        if tipo in CLASSES:
            g.add((uri, RDF.type, OWL.NamedIndividual))
            g.add((uri, RDF.type, CLASSES[tipo]))

        # Nome (data property, se existir)
        if "nome" in item:
            g.add((uri, BT.nome, Literal(item["nome"], datatype=XSD.string)))

        # Object properties
        for json_key, owl_prop in PROPS.items():
            if json_key in item and json_key != "tipo":
                value = item[json_key]
                if isinstance(value, list):
                    for v in value:
                        g.add((uri, owl_prop, BT[v]))
                else:
                    g.add((uri, owl_prop, BT[value]))

# Carregar os dois datasets
print("A carregar dataset_100.json...")
data = load_json("dataset_temporal.json")
add_individuals(data)
print(f"  → {len(data)} indivíduos adicionados")

# Guardar o resultado
output_path = "biblioteca_temporal_populated.ttl"
g.serialize(destination=output_path, format="turtle")
print(f"\nOntologia guardada em: {output_path}")
print(f"Total de triplos: {len(g)}")
