import json
from src.algorithms.baseline_algorithm import BaseLineAlgorithm


def getJson():
    with open('src/instances/grafo.json', 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)
    return data

def main():
    dados = getJson()
    baseLine = BaseLineAlgorithm(dados)
    AvgSpeed, AvgWaiting_time = baseLine.executarAlgoritmo()
    return AvgSpeed, AvgWaiting_time

main()