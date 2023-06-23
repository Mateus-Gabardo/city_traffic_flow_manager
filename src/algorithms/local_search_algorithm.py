import copy
import random
import itertools
import argparse
import json
from src.sumo_simulation import SumoSimulation

class LocalSearchAlgorithm:
    def __init__(self):
        pass

    @staticmethod
    def searchBestNeighbor(network, budget, estrategia, vehicles):
        no1, no2 = LocalSearchAlgorithm.getTwoRandomNodes(network)
        arestas_relacionadas = LocalSearchAlgorithm.getRelatedEdges(network, no1, no2)
        modificacoes = LocalSearchAlgorithm.generateValidCombinations(network, arestas_relacionadas, budget)

        min_tmax = float("inf")
        best_network = network
        primeira_melhoria = True

        for conjunto_arestas in modificacoes:
            new_network = LocalSearchAlgorithm.applyChanges(network, conjunto_arestas)

            simulador = SumoSimulation(new_network, vehicles)
            avgTravelTime = simulador.run_simulation()

            if min_tmax > avgTravelTime:
                best_network = new_network
                min_tmax = avgTravelTime
                if not primeira_melhoria and estrategia == 2:
                    return best_network, min_tmax

                primeira_melhoria = False

        return best_network, min_tmax

    @staticmethod
    def getTwoRandomNodes(network):
        nodes = list(network['vertices'])
        return random.sample(nodes, 2)

    @staticmethod
    def getRelatedEdges(network, no1, no2):
        arestas_relacionadas = []

        for aresta, dados in network["arestas"].items():
            extremos = aresta.split("-")
            if no1 in extremos or no2 in extremos:
                arestas_relacionadas.append(aresta)

        return arestas_relacionadas

    @staticmethod
    def generateValidCombinations(network, arestas_relacionadas, budget):
        modificacoes = []

        for r in range(1, len(arestas_relacionadas) + 1):
            combinacoes = list(itertools.combinations(arestas_relacionadas, r))
            

            for combinacao in combinacoes:
                comprimento_total = sum(network['arestas'][aresta]['length'] for aresta in combinacao)
                if comprimento_total <= budget:
                    modificacoes.append(combinacao)

        return modificacoes

    @staticmethod
    def applyChanges(network, conjunto_arestas):
        new_network = copy.deepcopy(network)

        for id_aresta in conjunto_arestas:
            json_aresta = new_network['arestas'][id_aresta]
            json_aresta["numLanes"] += 1
            new_network['arestas'][id_aresta] = json_aresta

        return new_network

    @staticmethod
    def initialSolution(network, budget, vehicles):
        new_network = network
        tentativas = len(network['arestas'])
        best_modificacoes = []

        while not best_modificacoes and tentativas > 0:
            arestas = list(network['arestas'].keys())
            aresta1, aresta2 = random.sample(arestas, 2)
            arestas_candidatas = [(aresta1), (aresta2)]

            modificacoes = LocalSearchAlgorithm.generateValidCombinations(network, arestas_candidatas, budget)

            if modificacoes:
                best_modificacoes = max(modificacoes, key=len)

            tentativas -= 1
            if tentativas == 0:
                break

        if best_modificacoes:
            new_network = LocalSearchAlgorithm.applyChanges(network, best_modificacoes)
            simulador = SumoSimulation(new_network, vehicles)
            avgTravelTime = simulador.run_simulation()
        else:
            avgTravelTime = None

        return new_network, avgTravelTime

    @staticmethod
    def localSearch(grafo, budget, interacoes=50, estrategia=2, vehicles = 50):
        best_network, best_temp = LocalSearchAlgorithm.initialSolution(grafo, budget, vehicles)

        qtd_iteracoes = interacoes

        while int(qtd_iteracoes) > 0:
            network_curent, temp_curent = LocalSearchAlgorithm.searchBestNeighbor(grafo, budget, estrategia, vehicles)
            if temp_curent < best_temp:
                best_temp = temp_curent
                best_network = network_curent
            qtd_iteracoes = qtd_iteracoes - 1

        return best_network, best_temp

    @staticmethod
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("--budget", type=float, default=50, help="representa o budget")
        parser.add_argument("--interation", type=int, default=10, help="Numero de iterações do algoritmo")
        parser.add_argument("--estrategy", type=int, default=2, help="Define a estrategia")
        return parser.parse_args()

    def run(self):
        args = LocalSearchAlgorithm.parse_args()

        with open('src/data/grid/grid.json', 'r') as f:
            json_str = f.read()
            data = json.loads(json_str)

        best_network, best_temp = LocalSearchAlgorithm.localSearch(data, args.budget, args.interation, args.estrategy, 50)

        print("Melhor solução encontrada:")
        print("Network:", best_network)
        print("Tempo de viagem médio:", best_temp)


if __name__ == "__main__":
    lsa = LocalSearchAlgorithm()
    lsa.run()
