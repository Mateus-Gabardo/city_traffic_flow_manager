import json
import math
import random
import copy
from src.sumo_simulation import SumoSimulation
from src.generators.sumo_xml_generator import SumoFilesGenerator
import xml.etree.ElementTree as ET

class BaseLineAlgorithm:
    def __init__(self, dados, nSimulation, budget):
        self.graph = dados
        self.simulation_number = nSimulation
        self.buget_number = budget
        self.buget_number = float(self.buget_number)

    def executar_algoritmo(self):
        
        modifications = []
        arestas_criadas = []
        simulacoes = int(self.simulation_number)
        json_inicial = self.graph
        bestJson = json_inicial

        # Retorno da simulação da instância inicial
        simulador = SumoSimulation(self.graph)
        BestAvgTravelTime = simulador.run_simulation()

        while simulacoes > 0:
            json_mod = copy.deepcopy(json_inicial)
            vertices = json_mod['vertices']
            coordenadas = json_mod['coordenadas']
            arestas = json_mod['arestas']
            current_modification = []
            budget = self.buget_number
            
            for i in range(2):
                
                if random.random() < 0.5:
                    json_mod, current_modification, budget = self.nova_lane(arestas, modifications, json_mod, current_modification, budget)
                   
                else:
                    json_mod, current_modification, budget = self.nova_aresta(vertices, arestas, arestas_criadas, coordenadas, json_mod, current_modification, budget)
            
            # Decrementar variável de critério de parada caso essa combinação não tiver sido feita
            alternative_modification = [current_modification[1], current_modification[0]]
            if current_modification not in modifications and alternative_modification not in modifications:
                modifications.append(current_modification)
                simulacoes -= 1

                print(f"Modificação: {modifications}")
                # Simular modificação
                simulador = SumoSimulation(json_mod)
                AvgTravelTime = simulador.run_simulation()

                # Verificar se a modificação resultou em uma melhora
                if AvgTravelTime < BestAvgTravelTime:
                    BestAvgTravelTime = AvgTravelTime
                    bestJson = json_mod

        # Printar a melhor melhora no final
        print(f'O melhor tempo de viagem foi: {BestAvgTravelTime}')

        return BestAvgTravelTime

    def nova_lane(self, arestas, modifications, json_mod, current_modification, budget):
         # escolha aleatoriamente uma das arestas
        aresta = random.choice(list(arestas.keys()))

        # verifique se essa aresta já foi modificada anteriormente
        while aresta in modifications:
            aresta = random.choice(list(arestas.keys()))
        
        # Verificar se está dento do budget
        distancia = json_mod["arestas"][aresta]["length"]
        if distancia <= budget:
            budget -= distancia

             # adicionar mais uma lane à aresta escolhida
            arestas[aresta]["numLanes"] += 1
            json_mod['arestas'] = arestas

            # adicionar a aresta escolhida na lista de modificações e diminuir do budget
            current_modification.append(aresta)

        return json_mod, current_modification, budget

    def nova_aresta(self, vertices, arestas, arestas_criadas, coordenadas, json_mod, current_modification, budget):
        tamanho_inicial = len(current_modification)
        while tamanho_inicial == len(current_modification):
            
            # escolher aleatoriamente uma possível nova aresta
            vertice = random.choice(list(vertices))
            arestas_possiveis = self.ret_nova_arestas(vertice, arestas, arestas_criadas, coordenadas)

            if len(arestas_possiveis) > 0:
                isok = False
                while not isok:
                    new_edge_name = random.choice(arestas_possiveis)

                    # Verificar se está dento do budget
                    distancia = 1
                    #json_mod["arestas"][new_edge_name]["length"]
                    if distancia <= budget:
                        budget -= distancia
                        isok = True
                        new_edge = {
                            "lenght": 20,
                            "maxSpeed": random.randint(30, 70),
                            "numLanes": 1,
                            "priority": random.randint(80, 100)
                        }
                        arestas[new_edge_name] = new_edge
                        json_mod['arestas'] = arestas
                        arestas_criadas.append(new_edge_name)
                        current_modification.append(new_edge_name)
                    else:
                        arestas_possiveis.remove(new_edge_name)
                        if not arestas_possiveis:
                            isok = True

        return json_mod, current_modification, budget

    def ret_nova_arestas(self, verticeOrigem, arestas, arestas_criadas, coordenadas):
        arestas_possiveis = set()
        for aresta in arestas:
            v1, v2 = aresta.split('-')
            if v1 == verticeOrigem and v2 not in arestas_criadas:
                for outra_aresta in arestas:
                    if v2 == outra_aresta.split('-')[0] and v1 != outra_aresta.split('-')[1]:
                        ponto1 = self.ret_coordenadas(v1, coordenadas)
                        ponto2 = self.ret_coordenadas(v2, coordenadas)
                        ponto3 = self.ret_coordenadas(outra_aresta.split('-')[1], coordenadas)
                        if not self.calcular_reta(ponto1, ponto2, ponto3):
                            arestas_possiveis.add(v1 + '-' + outra_aresta.split('-')[1])

        return list(arestas_possiveis)

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
        if ponto1[0] == ponto2[0] == x3 or ponto1[1] == ponto2[1] == y3:
            return True
        else:
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