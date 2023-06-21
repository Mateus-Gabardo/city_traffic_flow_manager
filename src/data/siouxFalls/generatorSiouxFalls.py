import json
from src.generators.grafo_generator import GrafoJsonWriter
from src.generators.sumo_xml_generator import SumoFilesGenerator
from src.generators.OD_matrix_converter import ODMatrixConverter
from src.generators.sumo_xml_demand_generator import SumoXmlDemandGenerator

def __gerar_instancia_sioux_falls():

    grafo = GrafoJsonWriter()

    atr = {
        1: {"length": 0.4, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        2: {"length": 0.3, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        3: {"length": 1.0, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        4: {"length": 0.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        5: {"length": 3.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        6: {"length": 0.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        7: {"length": 0.1, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        8: {"length": 0.4, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        9: {"length": 0.4, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        10: {"length": 0.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        11: {"length": 1.7, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        12: {"length": 1.7, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        13: {"length": 3.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        14: {"length": 1.7, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        15: {"length": 0.3, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        16: {"length": 0.9, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        17: {"length": 0.5, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        18: {"length": 0.2, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        19: {"length": 1.7, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        20: {"length": 3.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        21: {"length": 0.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        22: {"length": 1.1, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        23: {"length": 0.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        24: {"length": 0.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        25: {"length": 0.5, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        26: {"length": 0.5, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        27: {"length": 0.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        28: {"length": 3.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        29: {"length": 1.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        30: {"length": 0.5, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        31: {"length": 0.2, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        32: {"length": 0.6, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        33: {"length": 0.6, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        34: {"length": 0.3, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        35: {"length": 1.1, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        36: {"length": 0.6, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        37: {"length": 0.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        38: {"length": 1.9, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        39: {"length": 0.9, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        40: {"length": 0.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        41: {"length": 0.5, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        42: {"length": 2.9, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        43: {"length": 0.6, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        44: {"length": 0.5, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        45: {"length": 1.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        46: {"length": 1.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        47: {"length": 1.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        48: {"length": 1.6, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        49: {"length": 0.2, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        50: {"length": 0.6, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        51: {"length": 0.6, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        52: {"length": 0.2, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        53: {"length": 1.5, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        54: {"length": 2.9, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        55: {"length": 0.6, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        56: {"length": 0.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        57: {"length": 1.0, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        58: {"length": 0.7, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        59: {"length": 0.9, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        60: {"length": 0.5, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        61: {"length": 2.9, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        62: {"length": 0.9, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        63: {"length": 1.6, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        64: {"length": 0.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        65: {"length": 0.5, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        66: {"length": 1.6, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        67: {"length": 0.4, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        68: {"length": 0.7, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        69: {"length": 0.5, "maxSpeed": 25, "numLanes": 1, "priority": 100},
        70: {"length": 0.3, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        71: {"length": 0.7, "maxSpeed": 50, "numLanes": 3, "priority": 100},
        72: {"length": 0.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        73: {"length": 1.2, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        74: {"length": 0.3, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        75: {"length": 0.4, "maxSpeed": 25, "numLanes": 2, "priority": 100},
        76: {"length": 0.4, "maxSpeed": 25, "numLanes": 1, "priority": 100}
    }

    arestas = [
        ("1", "3", atr[2]),
        ("1", "2", atr[1]),
        ("2", "1", atr[3]),
        ("2", "6", atr[4]),
        ("3", "1", atr[5]),
        ("3", "4", atr[6]),
        ("3", "12", atr[7]),
        ("4", "3", atr[8]),
        ("4", "5", atr[9]),
        ("4", "11", atr[10]),
        ("5", "4", atr[11]),
        ("5", "6", atr[12]),
        ("5", "9", atr[13]),
        ("6", "2", atr[14]),
        ("6", "5", atr[15]),
        ("7", "8", atr[17]),
        ("7", "18", atr[18]),
        ("8", "6", atr[19]),
        ("8", "7", atr[20]),
        ("8", "9", atr[21]),
        ("8", "16", atr[22]),
        ("9", "8", atr[24]),
        ("9", "10", atr[25]),
        ("10", "9", atr[26]),
        ("10", "11", atr[27]),
        ("10", "15", atr[28]),
        ("10", "16", atr[29]),
        ("10", "17", atr[30]),
        ("11", "4", atr[31]),
        ("11", "10", atr[32]),
        ("11", "12", atr[33]),
        ("11", "14", atr[34]),
        ("12", "3", atr[35]),
        ("12", "11", atr[36]),
        ("13", "12", atr[38]),
        ("13", "24", atr[39]),
        ("14", "11", atr[40]),
        ("14", "15", atr[41]),
        ("14", "23", atr[42]),
        ("15", "10", atr[43]),
        ("15", "14", atr[44]),
        ("15", "19", atr[45]),
        ("15", "22", atr[46]),
        ("16", "8", atr[47]),
        ("16", "10", atr[48]),
        ("16", "17", atr[49]),
        ("16", "18", atr[50]),
        ("17", "10", atr[51]),
        ("17", "16", atr[52]),
        ("17", "19", atr[53]),
        ("18", "7", atr[54]),
        ("18", "16", atr[55]),
        ("18", "20", atr[56]),
        ("19", "15", atr[57]),
        ("19", "17", atr[58]),
        ("19", "20", atr[59]),
        ("20", "18", atr[60]),
        ("20", "19", atr[61]),
        ("20", "21", atr[62]),
        ("20", "22", atr[63]),
        ("21", "20", atr[64]),
        ("21", "22", atr[65]),
        ("21", "24", atr[66]),
        ("22", "15", atr[67]),
        ("22", "20", atr[68]),
        ("22", "21", atr[69]),
        ("22", "23", atr[70]),
        ("23", "14", atr[71]),
        ("23", "22", atr[72]),
        ("23", "24", atr[73]),
        ("24", "13", atr[74]),
        ("24", "21", atr[75]),
        ("24", "23", atr[76])
    ]

    eixos = [
        {"node": 1, "x": 500, "y": 5100},
        {"node": 2, "x": 3200, "y": 5100},
        {"node": 3, "x": 500, "y": 4400},
        {"node": 4, "x": 1300, "y": 4400},
        {"node": 5, "x": 2200, "y": 4400},
        {"node": 6, "x": 3200, "y": 4400},
        {"node": 7, "x": 4200, "y": 3800},
        {"node": 8, "x": 3200, "y": 3800},
        {"node": 9, "x": 2200, "y": 3800},
        {"node": 10, "x": 2200, "y": 3200},
        {"node": 11, "x": 1300, "y": 3200},
        {"node": 12, "x": 500, "y": 3200},
        {"node": 13, "x": 500, "y": 500},
        {"node": 14, "x": 1300, "y": 1900},
        {"node": 15, "x": 2200, "y": 1900},
        {"node": 16, "x": 3200, "y": 3200},
        {"node": 17, "x": 3200, "y": 2600},
        {"node": 18, "x": 4200, "y": 3200},
        {"node": 19, "x": 3200, "y": 1900},
        {"node": 20, "x": 3200, "y": 500},
        {"node": 21, "x": 2200, "y": 500},
        {"node": 22, "x": 2200, "y": 1300},
        {"node": 23, "x": 1300, "y": 1300},
        {"node": 24, "x": 1300, "y": 500}
    ]

    for origem, destino, atributo in arestas:
        grafo.adicionar_aresta(origem, destino, atributo)

    for item in eixos:
        grafo.adicionar_coordenadas(str(item["node"]), str(item["x"]), str(item["y"]))
    
    grafo.salvar_arquivo_json("siouxFalls.json", "src/data/siouxFalls")

def __gerarIntanciaSumo():
    with open('src/data/siouxFalls/siouxFalls.json', 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)
    
    grafoFile = SumoFilesGenerator(data)
    grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")

def __gerarDemandaOD(scala):
    inputFile = "src/data/siouxFalls/SiouxFalls_trips.tntp"
    outputFile = "src/data/siouxFalls/siouxFalls_taz.xml"
    ODConverter = ODMatrixConverter(inputFile, outputFile)
    ODConverter.convert_OD_matrix(scala)
    network_file = "src/sumo_data/network.net.xml"
    taz_file = "src/data/siouxFalls/siouxFalls_taz.xml"
    output_file = "src/sumo_data/routes.xml"
    demand_generator = SumoXmlDemandGenerator(network_file, output_file)
    demand_generator.generateDemandByTaz(taz_file)



def gerar_intancia_sioux_falls(scala):
    __gerar_instancia_sioux_falls()
    __gerarIntanciaSumo()
    __gerarDemandaOD(scala)