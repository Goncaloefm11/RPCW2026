import requests, argparse, os

def upload_to_graphdb(endpoint, repoID, file):
    if not os.path.exists(file):
        print(f"Erro: O ficheiro '{file}' não foi encontrado")
    else:
        url = f"{endpoint}/repositories/{repoID}/statements"
        headers = {"Content-Type": "text/turtle;charset=utf-8"}
        
        print(f"A ler o ficheiro '{file}'...")
        try:
            with open(file, 'r', encoding='utf-8') as f:
                ttl = f.read()
            
            print(f"A carregar os dados no repositório '{repoID}'...")
            response = requests.post(url, data=ttl.encode('utf-8'), headers=headers)
            
            if response.status_code in [200, 201, 204]:
                print("Dataset carregado com sucesso!")
            else:
                print(f"Erro ao carregar a informação: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Carregar um dataset Turtle (.ttl) no GraphDB")
    parser.add_argument("ficheiro", help="Caminho para o ficheiro .ttl")
    parser.add_argument("--repo", default="restaurante3", help="ID do repositorio no GraphDB")
    parser.add_argument("--url", default="http://localhost:7200", help="URL do GraphDB (default: http://localhost:7200)")

    args = parser.parse_args()
    upload_to_graphdb(args.url, args.repo, args.ficheiro)