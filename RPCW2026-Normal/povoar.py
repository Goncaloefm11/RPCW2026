import json
import re
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import OWL, XSD

# 1. Inicializar o Grafo e carregar a ontologia base
g = Graph()
# Carrega a estrutura base que definiste no primeiro passo
g.parse("sapientia_base.ttl", format="turtle")

# 2. Definir o Namespace
NS = Namespace("http://rpcw.di.uminho.pt/2025/sapientia/")
g.bind("", NS)

def g_uri(nome):
    """Função auxiliar para criar URIs válidas a partir de strings com espaços/acentos"""
    # Remove acentos e caracteres especiais simples, converte para snake_case
    nome_limpo = nome.lower().strip()
    nome_limpo = re.sub(r'[áàâãä]', 'a', nome_limpo)
    nome_limpo = re.sub(r'[éèêë]', 'e', nome_limpo)
    nome_limpo = re.sub(r'[íìîï]', 'i', nome_limpo)
    nome_limpo = re.sub(r'[óòôõö]', 'o', nome_limpo)
    nome_limpo = re.sub(r'[úùûü]', 'u', nome_limpo)
    nome_limpo = re.sub(r'[ç]', 'c', nome_limpo)
    nome_limpo = re.sub(r'[^a-z0-9_ ]', '', nome_limpo)
    nome_limpo = re.sub(r'\s+', '_', nome_limpo)
    return NS[nome_limpo]

def criar_individuo_minimo(uri, classe, nome_literal):
    """Garante que o indivíduo existe com a classe e o nome base (Regra do Enunciado)"""
    g.add((uri, RDF.type, OWL.NamedIndividual))
    g.add((uri, RDF.type, classe))
    g.add((uri, NS.nome, Literal(nome_literal, datatype=XSD.string)))

# ==========================================
# 3. Processar CONCEITOS
# ==========================================
try:
    with open("conceitos.json", "r", encoding="utf-8") as f:
        data_conceitos = json.load(f)
    for c in data_conceitos.get("conceitos", []):
        c_uri = g_uri(c["nome"])
        criar_individuo_minimo(c_uri, NS.Conceito, c["nome"])
        
        # Período Histórico
        if "períodoHistórico" in c and c["períodoHistórico"]:
            ph_uri = g_uri(c["períodoHistórico"])
            criar_individuo_minimo(ph_uri, NS.PeríodoHistorico, c["períodoHistórico"])
            g.add((c_uri, NS.surgeEm, ph_uri))
            
        # Aplicações
        for app in c.get("aplicações", []):
            app_uri = g_uri(app)
            criar_individuo_minimo(app_uri, NS.Aplicação, app)
            g.add((c_uri, NS.temAplicaçãoEm, app_uri))
            
        # Conceitos Relacionados
        for cr in c.get("conceitosRelacionados", []):
            cr_uri = g_uri(cr)
            criar_individuo_minimo(cr_uri, NS.Conceito, cr)
            g.add((c_uri, NS.estáRelacionadoCom, cr_uri))
except FileNotFoundError:
    print("Aviso: conceitos.json não encontrado.")

# ==========================================
# 4. Processar DISCIPLINAS
# ==========================================
try:
    with open("disciplinas.json", "r", encoding="utf-8") as f:
        data_disciplinas = json.load(f)
    for d in data_disciplinas.get("disciplinas", []):
        d_uri = g_uri(d["nome"])
        criar_individuo_minimo(d_uri, NS.Disciplina, d["nome"])
        
        # Tipos De Conhecimento
        for tc in d.get("tiposDeConhecimento", []):
            tc_uri = g_uri(tc)
            criar_individuo_minimo(tc_uri, NS.TipoDeConhecimento, tc)
            g.add((d_uri, NS.pertenceA, tc_uri))
            
        # Conceitos associados
        for conc in d.get("conceitos", []):
            conc_uri = g_uri(conc)
            criar_individuo_minimo(conc_uri, NS.Conceito, conc)
            g.add((conc_uri, NS.éEstudadoEm, d_uri))
except FileNotFoundError:
    print("Aviso: disciplinas.json não encontrado.")

# ==========================================
# 5. Processar MESTRES
# ==========================================
try:
    with open("mestres.json", "r", encoding="utf-8") as f:
        data_mestres = json.load(f)
    for m in data_mestres.get("mestres", []):
        m_uri = g_uri(m["nome"])
        criar_individuo_minimo(m_uri, NS.Mestre, m["nome"])
        
        # Disciplinas que ensina
        for disc in m.get("disciplinas", []):
            disc_uri = g_uri(disc)
            criar_individuo_minimo(disc_uri, NS.Disciplina, disc)
            g.add((m_uri, NS.ensina, disc_uri))
            
        # Período Histórico (se existir no mestre)
        if "períodoHistórico" in m and m["períodoHistórico"]:
            ph_uri = g_uri(m["períodoHistórico"])
            criar_individuo_minimo(ph_uri, NS.PeríodoHistorico, m["períodoHistórico"])
            # Nota: O enunciado original não sugeriu mestre->período, mas criamos o indivíduo
except FileNotFoundError:
    print("Aviso: mestres.json não encontrado.")

# ==========================================
# 6. Processar OBRAS
# ==========================================
try:
    with open("obras.json", "r", encoding="utf-8") as f:
        data_obras = json.load(f)
    for o in data_obras.get("obras", []):
        # Usamos o título como identificador da obra
        o_uri = g_uri(o["titulo"])
        g.add((o_uri, RDF.type, OWL.NamedIndividual))
        g.add((o_uri, RDF.type, NS.Obra))
        g.add((o_uri, NS.titulo, Literal(o["titulo"], datatype=XSD.string)))
        
        # Autor / Mestre
        if "autor" in o and o["autor"]:
            m_uri = g_uri(o["autor"])
            criar_individuo_minimo(m_uri, NS.Mestre, o["autor"])
            g.add((o_uri, NS.foiEscritoPor, m_uri))
            
        # Conceitos que explica
        for conc in o.get("conceitos", []):
            conc_uri = g_uri(conc)
            criar_individuo_minimo(conc_uri, NS.Conceito, conc)
            g.add((o_uri, NS.explica, conc_uri))
except FileNotFoundError:
    print("Aviso: obras.json não encontrado.")

# ==========================================
# 7. Processar APRENDIZES (Altere para o nome real do seu ficheiro JSON)
# ==========================================
# Nota: Ajuste o nome do ficheiro conforme o fornecido na pasta specific_datasets
nome_ficheiro_aprendiz = "pg61524.json" 

try:
    with open(nome_ficheiro_aprendiz, "r", encoding="utf-8") as f:
        data_aprendizes = json.load(f)
    for a in data_aprendizes:
        a_uri = g_uri(a["nome"])
        g.add((a_uri, RDF.type, OWL.NamedIndividual))
        g.add((a_uri, RDF.type, NS.Aprendiz))
        g.add((a_uri, NS.nome, Literal(a["nome"], datatype=XSD.string)))
        g.add((a_uri, NS.idade, Literal(int(a["idade"]), datatype=XSD.integer)))
        
        # Disciplinas que o aprendiz frequenta
        for disc in a.get("disciplinas", []):
            disc_uri = g_uri(disc)
            criar_individuo_minimo(disc_uri, NS.Disciplina, disc)
            g.add((a_uri, NS.aprende, disc_uri))
except FileNotFoundError:
    print(f"Aviso: Ficheiro de aprendiz '{nome_ficheiro_aprendiz}' nao encontrado. Altere a variavel no script.")

# ==========================================
# 8. Gravar o resultado em sapientia_ind.ttl
# ==========================================
g.serialize(destination="sapientia_ind.ttl", format="turtle")
print("Sucesso! O ficheiro 'sapientia_ind.ttl' foi gerado com todos os indivíduos.")