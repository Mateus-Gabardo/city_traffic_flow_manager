import json
from src.generators.grafo_generator import GrafoJsonWriter
from src.generators.sumo_xml_generator import SumoFilesGenerator
from src.generators.sumo_xml_router_generator import SumoXMLRouterGenerator

def __gerar_instancia_grid():
    grafo = GrafoJsonWriter()

    atributos = {
        1: {"length": 20, "maxSpeed": 80, "numLanes": 1, "priority": 100},
        2: {"length": 20, "maxSpeed": 60, "numLanes": 1, "priority": 100}
    }

    # Definindo as arestas
    grafo.adicionar_aresta("1", "2", atributos[1])
    grafo.adicionar_aresta("1", "4", atributos[1])
    grafo.adicionar_aresta("2", "1", atributos[1])
    grafo.adicionar_aresta("2", "5", atributos[2])
    grafo.adicionar_aresta("2", "3", atributos[1])
    grafo.adicionar_aresta("3", "6", atributos[1])
    grafo.adicionar_aresta("3", "2", atributos[1])
    grafo.adicionar_aresta("4", "1", atributos[1])
    grafo.adicionar_aresta("4", "7", atributos[1])
    grafo.adicionar_aresta("4", "5", atributos[2])
    grafo.adicionar_aresta("5", "4", atributos[2])
    grafo.adicionar_aresta("5", "8", atributos[2])
    grafo.adicionar_aresta("5", "2", atributos[2])
    grafo.adicionar_aresta("5", "6", atributos[2])
    grafo.adicionar_aresta("6", "9", atributos[1])
    grafo.adicionar_aresta("6", "5", atributos[2])
    grafo.adicionar_aresta("6", "3", atributos[1])
    grafo.adicionar_aresta("7", "4", atributos[1])
    grafo.adicionar_aresta("7", "8", atributos[1])
    grafo.adicionar_aresta("8", "5", atributos[2])
    grafo.adicionar_aresta("8", "9", atributos[1])

    # Definindo as coordenadas dos vértices
    grafo.adicionar_coordenadas("1", "-150.00", "150.00")
    grafo.adicionar_coordenadas("4", "0.00", "150.00")
    grafo.adicionar_coordenadas("7", "150.00", "150.00")
    grafo.adicionar_coordenadas("2", "-150.00", "0.00")
    grafo.adicionar_coordenadas("5", "0.00", "0.00")
    grafo.adicionar_coordenadas("8", "150.00", "0.00")
    grafo.adicionar_coordenadas("3", "-150.00", "-150.00")
    grafo.adicionar_coordenadas("6", "0.00", "-150.00")
    grafo.adicionar_coordenadas("9", "150.00", "-150.00")


    restricoes = {
        "1-5" : ["2-4", "4-2"],
        "2-4" : ["1-5", "5-1"],
        "2-6" : ["3-5", "5-3"],
        "3-5" : ["2-6", "6-2"],
        "4-8" : ["7-5", "5-7"],
        "5-7" : ["4-8", "8-4"],
        "5-9" : ["6-8", "8-6"],
        "6-8" : ["5-9", "6-8"],
    }
    grafo.adicionar_restricoes(restricoes)
    grafo.salvar_arquivo_json("grid.json", "src/data/grid")

def __gerarIntanciaSumo():
    with open('src/data/grid/grid.json', 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)
        
    grafoFile = SumoFilesGenerator(data)
    grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")
    
    demands = "src/data/grid/grid.trips.tntp"
    edges = "src/sumo_data/edges.xml"
    output = "src/data/grid/grid.rou.xml"
    #generator = SumoXMLRouterGenerator(demands, edges, output)
    #generator.generate_custom_sumo_routes_file()
    
def gerar_intancia_grid():
    __gerar_instancia_grid()
    __gerarIntanciaSumo()