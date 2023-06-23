
import random
import copy
from src.sumo_simulation import SumoSimulation
from src.generators.sumo_xml_generator import SumoFilesGenerator
import xml.etree.ElementTree as ET
import src.utils as util
import subprocess

class BaseLineAlgorithm2:
    def __init__(self, dados, nSimulation, budget):
        self.graph = dados
        self.simulation_number = nSimulation
        self.buget_number = budget

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
            budget = float(self.buget_number)
            
            for i in range(2):
                
                if random.random() < 0.5:
                    json_mod, current_modification, budget = util.nova_lane(arestas, modifications, json_mod, current_modification, budget)
                   
                else:
                    json_mod, current_modification, arestas_criadas, budget = util.nova_aresta(vertices, arestas, arestas_criadas, coordenadas, json_mod, current_modification, budget)
            
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
        command = ["python3", "sumo-gui", str(bestJson)]
        subprocess.call(command)

        return BestAvgTravelTime