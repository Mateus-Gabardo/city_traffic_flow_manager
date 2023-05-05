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
        simulacoes = int(self.simulation_number)

        # Retorno da simulação da instância inicial
        simulador = SumoSimulation(self.graph)
        BestAvgTravelTime = simulador.run_simulation()

        while simulacoes > 0:
            json_mod = self.graph
            vertices = json_mod['vertices']
            restricoes = json_mod['restricoes']
            coordenadas = json_mod['coordenadas']
            arestas = json_mod['arestas']
            current_modification = []
            bestJson = self.graph
            
            for i in range(2):
                
                if random.random() < 0.5:
                    json_mod, current_modification = self.novaLane(modifications, json_mod, current_modification)
                   
                else:
                    json_mod, current_modification = self.novaAresta(vertices, arestas, restricoes, arestas_criadas, coordenadas, json_mod, current_modification)
            
            # Decrementar variável de critério de parada caso essa combinação não tiver sido feita
            alternative_modification = [current_modification[1], current_modification[0]]
            if current_modification not in modifications and alternative_modification not in modifications:
                modifications.append(current_modification)
                simulacoes -= 1

                # Simular modificação
                simulador = SumoSimulation(json_mod)
                AvgTravelTime = simulador.run_simulation()

                # Verificar se a modificação resultou em uma melhora
                if AvgTravelTime < BestAvgTravelTime:
                    BestAvgTravelTime = AvgTravelTime
                    bestJson = json_mod

        # Printar a melhor melhora no final
        print(f'O melhor tempo de viagem foi: {bestJson}')

    def novaLane(arestas, modifications, json_mod, current_modification):
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

        return json_mod, current_modification

    def novaAresta(self, vertices, arestas, restricoes, arestas_criadas, coordenadas, json_mod, current_modification):
        while len(current_modification) == 0:
            # escolha aleatoriamente uma possível nova aresta
            vertice = random.choice(list(vertices))

            arestas_possiveis = self.ret_nova_arestas(vertice, arestas, restricoes, arestas_criadas, coordenadas)

            if len(arestas_possiveis) > 0:
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
        return json_mod, current_modification

    def ret_nova_arestas(self, verticeOrigem, arestas, restricoes, arestas_criadas, coordenadas):
        arestas_encontradas = []
        arestas_possiveis = []
        for aresta in arestas.keys():
            if aresta.split('-')[0] == verticeOrigem:
                arestas_encontradas.append(aresta)

        for aresta_encotrada in arestas_encontradas:
            for aresta in arestas.keys():
                if aresta_encotrada.split('-')[1] == aresta.split('-')[0] and aresta_encotrada.split('-')[0] != aresta.split('-')[1]:
                    ponto1 = self.ret_coordenadas(aresta_encotrada.split('-')[0], coordenadas)
                    ponto2 = self.ret_coordenadas(aresta.split('-')[1], coordenadas)
                    ponto3 = self.ret_coordenadas(aresta.split('-')[0], coordenadas)
                    if self.calcular_reta(ponto1, ponto2, ponto3) == False:
                        if aresta_encotrada.split('-')[0]+'-'+aresta.split('-')[1] not in arestas_possiveis:
                            arestas_possiveis.append(aresta_encotrada.split('-')[0]+'-'+aresta.split('-')[1])

        restricoes_aresta = restricoes.keys()
        for aresta_possivel in arestas_possiveis:
            if aresta_possivel in restricoes_aresta:
                arestas_possiveis.remove(aresta_possivel)
            if aresta_possivel in arestas_criadas:
                arestas_possiveis.remove(aresta_possivel)
        
        return arestas_possiveis

    def calcular_reta(self, ponto1, ponto2, ponto3):

        # Calcula a equação da reta y = mx + b, onde m é o coeficiente angular e b é o coeficiente linear.
        if ponto2[0] - ponto1[0] != 0:
            m = (ponto2[1] - ponto1[1]) / (ponto2[0] - ponto1[0])
            b = ponto1[1] - m * ponto1[0]
        else:
            # Caso a reta seja vertical, não há coeficiente angular e b é simplesmente o valor de x do ponto.
            m = float('inf')
            b = ponto1[0]

        # Verifica se o ponto 3 está na reta
        x3, y3 = ponto3
        if abs(y3 - (m * x3 + b)) < 1e-10:  # Usamos a função abs() para evitar problemas com coordenadas negativas
            return True
        else:
            return False

    def ret_coordenadas(self, vertice, coordenadas):
        for coordenada in coordenadas.keys():
            if vertice == coordenada:
                x = float(coordenadas[coordenada]["x"])
                y = float(coordenadas[coordenada]["y"])

        retorno = []
        retorno.append(x)
        retorno.append(y)
        return retorno