import json
import os 
import sys
from src.sumo_xml_generator import SumoFilesGenerator
import traci
import time
import xml.etree.ElementTree as ET
import shutil

sumo_path = shutil.which('sumo')
sumo_dir = os.path.dirname(sumo_path)

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

sumoBinary = sumo_dir+"/sumo"
sumoCmd = [sumoBinary, "-c", "src/instances/config.sumocfg"]

def callSumo(json_str):
    grafoFile = SumoFilesGenerator(json_str)
    grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")
    try:
        traci.start(sumoCmd)
    except traci.TraCIException:
        print("Erro ao conectar ao servidor TraCI, tentando novamente em 10 segundos...")
        time.sleep(10)
        #callSumo(json_str)
    
    SumSpeed = 0
    CountSpeed = 0
    SumWaiting_time= 0
    CountWaiting_time = 0

    # Faz uma simulação até que todos os veículos cheguem
    while traci.simulationStep():
 
        # obtém uma lista com os IDs de todos os veículos na rede
        veh_ids = traci.vehicle.getIDList()
    
        # itera sobre a lista de IDs dos veículos e coleta informações sobre cada um
        for veh_id in veh_ids:
            # obtém a posição do veículo
            x, y = traci.vehicle.getPosition(veh_id)
            
            # obtém a velocidade do veículo
            SumSpeed += traci.vehicle.getSpeed(veh_id)
            CountSpeed += 1
            
            # obtém o tempo de espera do veículo
            SumWaiting_time = traci.vehicle.getWaitingTime(veh_id)
            CountWaiting_time += 1

    traci.close()
    AvgSpeed = SumSpeed/CountSpeed
    AvgWaiting_time = SumWaiting_time/CountWaiting_time
    print('--------------------------------------------------------------------------------------------')
    print(f'finalizou simulação. Velocidade média:{AvgSpeed} e tempo de espera médio:{AvgWaiting_time}')
    print('--------------------------------------------------------------------------------------------')
    return AvgSpeed, AvgWaiting_time

def executarAlgoritmo():

    with open('grafo.json', 'r') as f:
        dados = json.load(f)
    
    arestas = dados['arestas']
    BestAvgSpeed, BestAvgWaiting_time = callSumo(dados)

    # Para cada Aresta será feita uma modificação e simulado novamente.
    # Caso seja uma melhora será salva. No final será alterado a melhor melhora.
    for nome in arestas.keys():
        json_mod = dados
        json_mod['arestas'][nome]['numLanes'] += 1
        #print(json_mod['arestas'][nome]['numLanes'])

        AvgSpeed, AvgWaiting_time = callSumo(json_mod)
        if AvgWaiting_time < BestAvgWaiting_time:
            BestAvgWaiting_time = AvgWaiting_time
            bestJson = json_mod
    
    print(bestJson)

executarAlgoritmo()