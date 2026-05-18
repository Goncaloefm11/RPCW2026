import json
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import OWL, XSD

# Configuração com o teu ID oficial
ALUNO_ID = "PG61524" 
BASE_IRI = f"http://www.di.uminho.pt/rpcw2026/{ALUNO_ID}/"

g = Graph()
g.parse("boardgames_base.ttl", format="turtle")
NS = Namespace(BASE_IRI)
g.bind("", NS)

def criar_no_seguro(id_str, classe):
    uri = NS[id_str]
    g.add((uri, RDF.type, OWL.NamedIndividual))
    g.add((uri, RDF.type, classe))
    return uri

# 1. Povoar Jogos
with open("jogos.json", "r", encoding="utf-8") as f:
    jogos = json.load(f)
for j in jogos:
    j_uri = criar_no_seguro(j["id"], NS.Game)
    g.add((j_uri, NS.id, Literal(j["id"], datatype=XSD.string)))
    g.add((j_uri, NS.name, Literal(j["name"], datatype=XSD.string)))
    g.add((j_uri, NS.category, Literal(j["category"], datatype=XSD.string)))
    g.add((j_uri, NS.minPlayers, Literal(int(j["minPlayers"]), datatype=XSD.integer)))
    g.add((j_uri, NS.maxPlayers, Literal(int(j["maxPlayers"]), datatype=XSD.integer)))
    g.add((j_uri, NS.playingTimeMinutes, Literal(int(j["playingTimeMinutes"]), datatype=XSD.integer)))
    g.add((j_uri, NS.descriptionEN, Literal(j["descriptionEN"], datatype=XSD.string)))

# 2. Povoar Autores
with open("autores.json", "r", encoding="utf-8") as f:
    autores = json.load(f)
for a in autores:
    a_uri = criar_no_seguro(a["id"], NS.Designer)
    g.add((a_uri, NS.id, Literal(a["id"], datatype=XSD.string)))
    g.add((a_uri, NS.name, Literal(a["name"], datatype=XSD.string)))
    for g_id in a.get("designedGames", []):
        criar_no_seguro(g_id, NS.Game)
        g.add((a_uri, NS.designedGame, NS[g_id]))

# 3. Povoar Editoras
with open("editoras.json", "r", encoding="utf-8") as f:
    editoras = json.load(f)
for e in editoras:
    e_uri = criar_no_seguro(e["id"], NS.Publisher)
    g.add((e_uri, NS.id, Literal(e["id"], datatype=XSD.string)))
    g.add((e_uri, NS.name, Literal(e["name"], datatype=XSD.string)))
    g.add((e_uri, NS.country, Literal(e["country"], datatype=XSD.string)))
    for g_id in e.get("publishedGames", []):
        criar_no_seguro(g_id, NS.Game)
        g.add((e_uri, NS.publishedGame, NS[g_id]))

# 4. Povoar Mecânicas
with open("mecanicas.json", "r", encoding="utf-8") as f:
    mecanicas = json.load(f)
for m in mecanicas:
    m_uri = criar_no_seguro(m["id"], NS.Mechanic)
    g.add((m_uri, NS.id, Literal(m["id"], datatype=XSD.string)))
    g.add((m_uri, NS.name, Literal(m["name"], datatype=XSD.string)))
    for g_id in m.get("usedInGames", []):
        criar_no_seguro(g_id, NS.Game)
        g.add((m_uri, NS.usedInGame, NS[g_id]))

# 5. Povoar Prémios
with open("premios.json", "r", encoding="utf-8") as f:
    premios = json.load(f)
for p in premios:
    p_uri = criar_no_seguro(p["id"], NS.Award)
    g.add((p_uri, NS.id, Literal(p["id"], datatype=XSD.string)))
    g.add((p_uri, NS.name, Literal(p["name"], datatype=XSD.string)))
    g.add((p_uri, NS.year, Literal(int(p["year"]), datatype=XSD.integer)))
    if "wonByGame" in p:
        criar_no_seguro(p["wonByGame"], NS.Game)
        g.add((p_uri, NS.wonByGame, NS[p["wonByGame"]]))

g.serialize(destination="boardgames_ind.ttl", format="turtle")
print("Ontologia 'boardgames_ind.ttl' povoada com as URIs de PG61524!")