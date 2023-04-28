import json
from src.sumo_simulation import SumoSimulation
from src.sumo_xml_generator import SumoFilesGenerator
import xml.etree.ElementTree as ET

class BaseLineAlgorithm:
    def __init__(self, dados):
        self.graph = dados

    def executarAlgoritmo(self):
        simulador = SumoSimulation(self.graph)
        arestas = self.graph['arestas']
        BestAvgTravelTime= simulador.run_simulation()

        # Para cada Aresta será feita uma modificação e simulado novamente.
        # Caso seja uma melhora será salva. No final será alterado a melhor melhora.
        for nome in arestas.keys():
            json_mod = self.graph
            json_mod['arestas'][nome]['numLanes'] += 1
            #print(json_mod['arestas'][nome]['numLanes'])
            simulador = SumoSimulation(self.graph)
            AvgTravelTime = simulador.run_simulation()
            if AvgTravelTime < BestAvgTravelTime:
                BestAvgTravelTime = AvgTravelTime
                bestJson = json_mod
        
        print(bestJson)