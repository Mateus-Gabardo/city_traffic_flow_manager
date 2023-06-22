import os
import subprocess
import sys
import shutil
from src.generators.sumo_xml_demand_generator import SumoXmlDemandGenerator
from src.generators.sumo_xml_generator import SumoFilesGenerator
import sumolib


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

        demand_generator = SumoXmlDemandGenerator(network_file, output_file)

        # Gera a demanda de maneira aleatória mas com um seed randomico
        demand_generator.generateDemand(num_trips, trip_depart_period, random_seed)

    
    def __average_speed(self):
        speedSum = 0.0
        edgeCount = 0
        for edge in sumolib.xml.parse('src/sumo_data/output.xml', ['edge']):
            speedSum += float(edge.traveltime)
            edgeCount += 1
        avgSpeed = speedSum / edgeCount
        #A velocidade média na borda/faixa dentro do intervalo relatado.
        print('Velocidade média da simulação:', avgSpeed)
        return avgSpeed

    def __run_sumo(self):
        output_file = "src/sumo_data/output.xml"
        command = self.sumoCmd + ["--edgedata-output", output_file]
        subprocess.call(command)
    


    def run_simulation(self):
        # Gerar os arquivos de configuração e de rotas
        grafoFile = SumoFilesGenerator(self.json_str)
        grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")

        self.gerarRotas()

        # Executamos o sumo
        self.__run_sumo()
        return self.__average_speed()



