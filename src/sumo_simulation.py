import os
import sys
import shutil
from src.generators.sumo_xml_demand_generator import SumoXmlDemandGenerator
import traci
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
        self.sumoCmd = [self.sumoBinary, "-c", "src/sumo_data/config.sumocfg"]
        self.json_str = json_str
    
    def gerarRotas(self):
        network_file = "src/sumo_data/network.net.xml"
        output_file = "src/sumo_data/routes.xml"
        num_trips = 50
        trip_depart_period = 1
        random_seed = 42

        demand_generator = SumoXmlDemandGenerator(network_file, output_file, num_trips, trip_depart_period, random_seed)

        # Gera a demanda de maneira aleatória mas com um seed randomico
        demand_generator.generateDemand()

    def run_simulation(self):
        # Gerar os arquivos de configuração e de rotas
        grafoFile = SumoFilesGenerator(self.json_str)
        grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")

        self.gerarRotas()

        # Iniciar a simulação
        try:
            traci.start(self.sumoCmd)
        except traci.TraCIException:
            print("Erro ao conectar ao servidor TraCI")
            return None

        SumTravelTime = 0
        CountTravelTime = 0

        # Fazer a simulação até que todos os veículos cheguem ao destino
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            veh_ids = traci.vehicle.getIDList()
            for veh_id in veh_ids:
                # Obter o tempo de viagem do veículo
                SumTravelTime += traci.vehicle.getAdaptedTraveltime(veh_id, traci.simulation.getTime(), traci.vehicle.getRoadID(veh_id))
                CountTravelTime += 1

        # Encerrar a simulação e calcular o tempo médio de viagem
        traci.close()
        AvgTravelTime = SumTravelTime / CountTravelTime

        print('--------------------------------------------------------------------------------------------')
        print(f'Finalizou simulação. Tempo de Viagem: {AvgTravelTime:.2f}')
        print('--------------------------------------------------------------------------------------------')

        return AvgTravelTime

