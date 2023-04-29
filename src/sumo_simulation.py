import os
import sys
import shutil
import traci
import time
import xml.etree.ElementTree as ET
from src.generators.sumo_xml_generator import SumoFilesGenerator


class SumoSimulation:
    def __init__(self, json_str):
        sumo_path = shutil.which('sumo')
        self.sumo_dir = os.path.dirname(sumo_path)

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        self.sumoBinary = os.path.join(self.sumo_dir, "sumo")
        self.sumoCmd = [self.sumoBinary, "-c", "src/instances/config.sumocfg"]
        self.json_str = json_str

    def run_simulation(self):
        grafoFile = SumoFilesGenerator(self.json_str)
        grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")
        try:
            traci.start(self.sumoCmd)
        except traci.TraCIException:
            print("Erro ao conectar ao servidor TraCI")
        
        self.confVehicle()

        SumTravelTime= 0
        CountTravelTime = 0

        # Faz uma simulação até que todos os veículos cheguem
        while traci.simulationStep():
            veh_ids = traci.vehicle.getIDList()
            for veh_id in veh_ids:
                
                # obtém o tempo de viagem do veículo
                SumTravelTime += traci.vehicle.getAdaptedTraveltime(veh_id)
                CountTravelTime += 1

        traci.close()
        AvgTravelTime = SumTravelTime/CountTravelTime
        print('--------------------------------------------------------------------------------------------')
        print(f'finalizou simulação. Tempo de Viagem:{AvgTravelTime}')
        print('--------------------------------------------------------------------------------------------')
        return AvgTravelTime
