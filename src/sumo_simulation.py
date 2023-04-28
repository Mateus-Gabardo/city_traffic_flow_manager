import os
import sys
import shutil
from src.sumo_vehicle_router import SumoVehicleRouter
import traci
import time
import xml.etree.ElementTree as ET
from src.sumo_xml_generator import SumoFilesGenerator


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
    
    def confVehicle(self):
        #Aqui depois será setrado a instancia
        router = SumoVehicleRouter(seed=42, min_speed=10, max_speed=30, accel=2, decel=4)
        router.set_vehicle_routes(num_vehicles=10)

    def run_simulation(self):
        grafoFile = SumoFilesGenerator(self.json_str)
        grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")
        try:
            traci.start(self.sumoCmd)
        except traci.TraCIException:
            print("Erro ao conectar ao servidor TraCI")
        
        self.confVehicle()

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
                SumWaiting_time += traci.vehicle.getWaitingTime(veh_id)
                CountWaiting_time += 1

        traci.close()
        AvgSpeed = SumSpeed/CountSpeed
        AvgWaiting_time = SumWaiting_time/CountWaiting_time
        print('--------------------------------------------------------------------------------------------')
        print(f'finalizou simulação. Velocidade média:{AvgSpeed} e tempo de espera médio:{AvgWaiting_time}')
        print('--------------------------------------------------------------------------------------------')
        return AvgSpeed, AvgWaiting_time
