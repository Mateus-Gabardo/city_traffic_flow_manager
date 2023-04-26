import os 
import sys
from src.sumo_xml_generator import SumoFilesGenerator
import traci
import time
import xml.etree.ElementTree as ET
import shutil

sumo_path = shutil.which('sumo')
sumo_dir = os.path.dirname(sumo_path)
print(sumo_dir)

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


def executeAlgoritm():

    # Faz uma simulação até que todos os veículos cheguem
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
    traci.close()
    print('finalizou')

def main():
    configFile()
    try:
        traci.start(sumoCmd)
    except traci.TraCIException:
        print("Erro ao conectar ao servidor TraCI, tentando novamente em 10 segundos...")
        time.sleep(10)
        main()
    executeAlgoritm()

main()