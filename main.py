import os 
import sys
from src.sumo_xml_generator import SumoFilesGenerator
from src.algorithms import baseline
import traci
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

def configFile():
    with open('src/instances/grafo.json', 'r') as f:
        json_str = f.read()
    grafoFile = SumoFilesGenerator(json_str)
    grafoFile.generateSumoFile(file_name_edge="edges.edg.xml", file_name_node="nodes.nod.xml")


def runSimulation(config):
    try:
        traci.start(config)
    except traci.TraCIException:
        print("Erro ao conectar ao servidor TraCI")

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
    print(f'finalizou simulação. Velocidade média:{AvgSpeed} e tempo de espera médio:{AvgWaiting_time}')

def main():
    configFile()
    runSimulation(sumoCmd)
def main(json_str):
    configFile(json_str)
    try:
        traci.start(sumoCmd)
    except traci.TraCIException:
        print("Erro ao conectar ao servidor TraCI, tentando novamente em 10 segundos...")
        time.sleep(10)
        main()
    AvgSpeed, AvgWaiting_time = executeAlgoritm()
    return AvgSpeed, AvgWaiting_time

#main()