import sys
from rdflib import Graph

def main():
    if len(sys.argv) < 3:
        print("\n ERROR: Argumentos insuficientes")
        print("Uso: python load_serialize.py <ficheiro_entrada> <formato_saida>")
        print("Formatos sugeridos: ttl, xml, json-ld, nt, n3\n")
    else:
        input_file = sys.argv[1]
        output_format = sys.argv[2].lower()
    
        g = Graph()
    
    try:
        g.parser(input_file)
        print(g.serialize(format=output_format))

    except FileNotFoundError:
        print(f"Erro: O ficheiro '{input_file}', não foi encontrado")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    main()