
from src.instances.network.uteis.grafo_generator import GrafoGenerator

def gerar():
    # Exemplo de uso
    grafo = GrafoGenerator()

    grafo.adicionar_aresta("A", "B", {"lenght": 10, "maxSpeed": 60, "numLanes" : 1})
    grafo.adicionar_aresta("B", "C", {"lenght": 8, "maxSpeed": 50, "numLanes" : 2})
    grafo.adicionar_aresta("C", "D", {"lenght": 12, "maxSpeed": 40, "numLanes" : 2})
    grafo.adicionar_aresta("D", "E", {"lenght": 15, "maxSpeed": 30, "numLanes" : 1})
    grafo.adicionar_aresta("E", "A", {"lenght": 5, "maxSpeed": 20, "numLanes" : 2})

    # Especificar a pasta destino para salvar o arquivo
    pasta_destino = "src/instances/network"
    # Chamar o método para salvar o grafo em arquivo, passando o nome do arquivo e a pasta destino
    grafo.salvar_grafo_em_arquivo("grafo.json", pasta_destino)

gerar()
    
