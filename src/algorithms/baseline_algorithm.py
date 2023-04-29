import json
import random
from src.sumo_simulation import SumoSimulation
from src.sumo_xml_generator import SumoFilesGenerator
import xml.etree.ElementTree as ET

class BaseLineAlgorithm:
    def __init__(self, dados, nSimulation):
        self.graph = dados
        self.simulation_number = nSimulation

    def executarAlgoritmo(self):
        
        modifications = []

        # Retorno da simulação da instância inicial
        simulador = SumoSimulation(self.graph)
        BestAvgTravelTime = simulador.run_simulation()

        while self.simulation_number > 0:
            json_mod = self.graph
            vertices = json_mod['vertices']
            arestas = json_mod['arestas']

            # Escolhendo aleatoriamente uma das arestas
            aresta = random.choice(list(arestas.keys()))

            # verifique se essa aresta já foi modificada anteriormente
            isMod = False
            for random_edge in modifications:
                if random_edge == aresta:
                    isMod = True
            
            if isMod == False:

                # adicione a aresta escolhida na lista de modificações
                modifications.append(aresta)

                if random.random() < 0.5:
                    # adicione mais uma lane à aresta escolhida
                    arestas[aresta]["numLanes"] += 1
                else:
                    # escolha aleatoriamente um vértice não utilizado
                    new_vertex = None
                    while new_vertex is None or new_vertex in vertices:
                        new_vertex = random.choice(vertices)

                    # crie uma nova aresta conectando a aresta escolhida a um novo vértice
                    new_edge_name = aresta[0] +'-'+ new_vertex
                    new_edge = {
                        "lenght": random.randint(5, 20),
                        "maxSpeed": random.randint(30, 70),
                        "numLanes": 1,
                        "priority": 100
                    }
                    arestas[new_edge_name] = new_edge

                    # Para cada Aresta será feita uma modificação e simulado novamente.
                    # Caso seja uma melhora será salva. No final será alterado a melhor melhora.
                    simulador = SumoSimulation(json_mod)
                    AvgTravelTime = simulador.run_simulation()

                    # Descrementar variável de critério de parada
                    self.simulation_number -= 1

                    # Verificar se a modificação resultou em uma melhora
                    if AvgTravelTime < BestAvgTravelTime:
                        BestAvgTravelTime = AvgTravelTime
                        bestJson = json_mod
                    
                    # Printar a melhor melhora no final
                    print(bestJson)