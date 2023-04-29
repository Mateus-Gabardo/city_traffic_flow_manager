import json
import random
from src.sumo_simulation import SumoSimulation
from src.generators.sumo_xml_generator import SumoFilesGenerator
import xml.etree.ElementTree as ET

class BaseLineAlgorithm:
    def __init__(self, dados, nSimulation):
        self.graph = dados
        self.simulation_number = nSimulation

    def executar_algoritmo(self):
        
        modifications = [[]]
        arestas_criadas = []

        # Retorno da simulação da instância inicial
        simulador = SumoSimulation(self.graph)
        BestAvgTravelTime = simulador.run_simulation()

        while self.simulation_number > 0:
            json_mod = self.graph
            vertices = json_mod['vertices']
            restricoes = json_mod['restricoes']
            coordenadas = json_mod['coordenadas']

            for i in range(2):
                current_modification = []
                arestas = json_mod['arestas']
                if random.random() < 0.5:

                    # escolha aleatoriamente uma das arestas
                    aresta = random.choice(list(arestas.keys()))

                    # verifique se essa aresta já foi modificada anteriormente
                    while aresta in modifications:
                        aresta = random.choice(list(arestas.keys()))
                    
                    # adicione mais uma lane à aresta escolhida
                    arestas[aresta]["numLanes"] += 1
                    json_mod['arestas'] = arestas

                    # adicione a aresta escolhida na lista de modificações
                    current_modification.append(aresta)
                else:
                    # escolha aleatoriamente uma possível nova aresta
                    vertice = random.choice(list(vertices.keys()))

                    arestas_possiveis = self.ret_nova_arestas(vertice, arestas, restricoes, arestas_criadas, coordenadas)

                    new_edge_name = random.choice(arestas_possiveis)
                    new_edge = {
                        "lenght": random.randint(5, 20),
                        "maxSpeed": random.randint(30, 70),
                        "numLanes": 1,
                        "priority": 100
                    }
                    arestas[new_edge_name] = new_edge
                    json_mod['arestas'] = arestas
                    arestas_criadas.append(new_edge_name)
                    current_modification.append(new_edge_name)
            
            # Decrementar variável de critério de parada caso essa combinação não tiver sido feita
            alternative_modification = [current_modification[1], current_modification[0]]
            if current_modification not in modifications and alternative_modification not in modifications:
                self.simulation_number -= 1

                # Simular modificação
                simulador = SumoSimulation(json_mod)
                AvgTravelTime = simulador.run_simulation()

                # Verificar se a modificação resultou em uma melhora
                if AvgTravelTime < BestAvgTravelTime:
                    BestAvgTravelTime = AvgTravelTime
                    bestJson = json_mod

        # Printar a melhor melhora no final
        print(bestJson)


    def ret_nova_arestas(self, verticeOrigem, arestas, restricoes, arestas_criadas, coordenadas):
        arestas_possiveis = []
        for aresta, vertices in arestas.items():
            if vertices[0] == verticeOrigem:
                for aresta2, vertices2 in arestas.items():
                    if vertices[1] == vertices2[0]:
                        ponto1 = coordenadas[vertices[0]]
                        ponto2 = coordenadas[vertices[1]]
                        ponto3 = coordenadas[vertices2[1]]
                        if not self.calcular_reta(ponto1, ponto2, ponto3):
                            nova_aresta = f"{vertices[0]}-{vertices2[1]}"
                            if nova_aresta not in restricoes and nova_aresta not in arestas_criadas:
                                arestas_possiveis.append(nova_aresta)
        return arestas_possiveis

    def calcular_reta(self, ponto1, ponto2, ponto3):
        # Calcula os coeficientes da reta y = mx + b
        delta_x = ponto2[0] - ponto1[0]
        delta_y = ponto2[1] - ponto1[1]
        m = delta_y / delta_x
        b = ponto1[1] - m * ponto1[0]
        # Verifica se o ponto está na reta y = mx + b
        y_calculado = m * ponto3[0] + b
        return abs(ponto3[1] - y_calculado) < 1e-6

    def ret_coordenadas(self, vertice, coordenadas):
        return coordenadas[vertice]
