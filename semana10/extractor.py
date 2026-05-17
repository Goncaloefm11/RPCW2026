import json
import sys
import ssl
from SPARQLWrapper import SPARQLWrapper, JSON

def run_extractor(query_file, output_file):
    # 1. Resolver problema de SSL (SoluÃ§Ã£o de emergÃªncia para ambientes de aula)
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except AttributeError:
        pass

    # 2. Ler a query do ficheiro de texto
    try:
        with open(query_file, 'r', encoding='utf-8') as f:
            query_string = f.read()
    except FileNotFoundError:
        print(f"Erro: O ficheiro de query '{query_file}' não foi encontrado.")
        return

    # 3. Configurar o Endpoint da DBpedia
    endpoint_url = "https://dbpedia.org/sparql"
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)

    try:
        print(f"A ler query de: {query_file}...")
        print("A enviar query para a DBpedia...")
        
        results = sparql.query().convert()
        
        # 4. Processar os resultados
        # Nota: Esta parte assume que a query usa variÃ¡veis no SELECT. 
        # Criamos um dataset genÃ©rico com todas as chaves retornadas.
        dataset = []
        for result in results["results"]["bindings"]:
            item = {var: result[var]["value"] for var in result.keys()}
            dataset.append(item)

        # 5. Guardar o ficheiro JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
            
        print(f"Sucesso! {len(dataset)} registos guardados em '{output_file}'.")

    except Exception as e:
        print(f"Erro durante a execuÃ§Ã£o: {e}")

if __name__ == "__main__":
    # Verifica se os dois argumentos foram passados
    if len(sys.argv) != 3:
        print("Uso correto: python extractor.py <ficheiro_query.sparql> <ficheiro_saida.json>")
    else:
        file_in = sys.argv[1]
        file_out = sys.argv[2]
        run_extractor(file_in, file_out)