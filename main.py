import json

from src.algorithms.baseline_algorithm import BaseLineAlgorithm


def getJson():
    with open('src/data/grid/grid.json', 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)
    return data

def main():
    dados = getJson()
    baseLine = BaseLineAlgorithm(dados, 100)
    AvgWaiting_time = baseLine.executar_algoritmo()
    print(AvgWaiting_time)

main()