import json
from src.generators.grafo_generator import GrafoJsonWriter
from src.generators.sumo_xml_generator import SumoFilesGenerator

def __gerar_instancia_grid():
    grafo = GrafoJsonWriter()

    atributos = {
        1: {"length": 20, "maxSpeed": 80, "numLanes": 1, "priority": 100},
        2: {"length": 20, "maxSpeed": 60, "numLanes": 1, "priority": 80}
    }

    arestas = [
        ("1", "2", atributos[1]),
        ("1", "5", atributos[2]),
        ("2", "1", atributos[2]),
        ("2", "6", atributos[2]),
        ("2", "3", atributos[1]),
        ("3", "2", atributos[2]),
        ("3", "7", atributos[1]),
        ("3", "4", atributos[2]),
        ("4", "3", atributos[2]),
        ("4", "8", atributos[2]),
        ("5", "1", atributos[2]),
        ("5", "6", atributos[2]),
        ("5", "9", atributos[2]),
        ("6", "5", atributos[2]),
        ("6", "2", atributos[2]),
        ("6", "10", atributos[2]),
        ("6", "7", atributos[2]),
        ("7", "6", atributos[2]),
        ("7", "3", atributos[2]),
        ("7", "11", atributos[1]),
        ("7", "8", atributos[2]),
        ("8", "7", atributos[2]),
        ("8", "4", atributos[2]),
        ("8", "12", atributos[2]),
        ("9", "5", atributos[2]),
        ("9", "13", atributos[2]),
        ("9", "10", atributos[2]),
        ("10", "9", atributos[2]),
        ("10", "6", atributos[2]),
        ("10", "14", atributos[2]),
        ("10", "11", atributos[2]),
        ("11", "10", atributos[2]),
        ("11", "7", atributos[2]),
        ("11", "15", atributos[1]),
        ("11", "12", atributos[2]),
        ("12", "11", atributos[2]),
        ("12", "8", atributos[2]),
        ("12", "16", atributos[2]),
        ("13", "9", atributos[2]),
        ("13", "14", atributos[2]),
        ("14", "10", atributos[2]),
        ("14", "15", atributos[2]),
        ("15", "11", atributos[2]),
        ("15", "16", atributos[2]),
        ("16", "15", atributos[2]),
        ("16", "12", atributos[2])
    ]

    for origem, destino, atributo in arestas:
        grafo.adicionar_aresta(origem, destino, atributo)


    # Definindo as coordenadas dos vértices
    grafo.adicionar_coordenadas("1", "-150.00", "150.00")
    grafo.adicionar_coordenadas("2", "-50.00", "150.00")
    grafo.adicionar_coordenadas("3", "50.00", "150.00")
    grafo.adicionar_coordenadas("4", "150.00", "150.00")

    grafo.adicionar_coordenadas("5", "-150.00", "50.00")
    grafo.adicionar_coordenadas("6", "-50.00", "50.00")
    grafo.adicionar_coordenadas("7", "50.00", "50.00")
    grafo.adicionar_coordenadas("8", "150.00", "50.00")

    grafo.adicionar_coordenadas("9", "-150.00", "-50.00")
    grafo.adicionar_coordenadas("10", "-50.00", "-50.00")
    grafo.adicionar_coordenadas("11", "50.00", "-50.00")
    grafo.adicionar_coordenadas("12", "150.00", "-50.00")

    grafo.adicionar_coordenadas("13", "-150.00", "-150.00")
    grafo.adicionar_coordenadas("14", "-50.00", "-150.00")
    grafo.adicionar_coordenadas("15", "50.00", "-150.00")
    grafo.adicionar_coordenadas("16", "150.00", "-150.00")


    restricoes = {
        "1-6" : ["2-5", "5-2"],
        "2-5" : ["1-6", "6-1"],
        "2-7" : ["3-6", "6-3"],
        "3-6" : ["2-7", "7-2"],
        "3-8" : ["7-4", "4-7"],
        "4-7" : ["3-8", "8-3"],
        "5-10" : ["6-9", "9-6"],
        "6-9" : ["5-10", "10-5"],
        "6-11" : ["7-10", "10-7"],
        "7-10" : ["6-11", "11-6"],
        "7-12" : ["8-11", "11-8"],
        "8-11" : ["7-12", "12-7"],
        "9-14" : ["10-13", "13-10"],
        "10-13" : ["9-14", "14-9"],
        "10-15" : ["11-14", "14-11"],
        "11-14" : ["10-15", "15-10"],
        "11-16" : ["12-15", "15-12"],
        "12-15" : ["11-16", "16-11"],        
    }
    
    grafo.adicionar_restricoes(restricoes)
    grafo.salvar_arquivo_json("grid.json", "src/data/grid")

def __gerarIntanciaSumo():
    with open('src/data/grid/grid.json', 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)
        
    grafoFile = SumoFilesGenerator(data)
    grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")
    
def gerar_intancia_grid():
    __gerar_instancia_grid()
    __gerarIntanciaSumo()