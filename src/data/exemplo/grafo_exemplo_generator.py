from src.generators.grafo_generator import GrafoJsonWriter

def __gerar_instancia_exemplo():
    grafo = GrafoJsonWriter()

    grafo.adicionar_aresta("A", "B", {"lenght": 10, "maxSpeed": 60, "numLanes" : 1, "priority": 100})
    grafo.adicionar_aresta("B", "C", {"lenght": 8, "maxSpeed": 50, "numLanes" : 2, "priority": 100})
    grafo.adicionar_aresta("C", "D", {"lenght": 12, "maxSpeed": 40, "numLanes" : 2, "priority": 100})
    grafo.adicionar_aresta("D", "E", {"lenght": 15, "maxSpeed": 30, "numLanes" : 1, "priority": 100})
    grafo.adicionar_aresta("E", "A", {"lenght": 5, "maxSpeed": 20, "numLanes" : 2, "priority": 100})

    nome_arquivo = "grafo.json"
    pasta_destino = "src/data/exemplo"
    grafo.salvar_arquivo_json(nome_arquivo, pasta_destino)

def gerar_instancia_exemplo():
    __gerar_instancia_exemplo()
