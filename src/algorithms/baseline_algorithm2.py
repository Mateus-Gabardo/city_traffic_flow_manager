import os
import shutil
import sys
import random
import copy
from src.sumo_simulation import SumoSimulation
from src.generators.sumo_xml_generator import SumoFilesGenerator
import xml.etree.ElementTree as ET
import src.utils as util
import subprocess
import tkinter as tk
import io
import contextlib
import concurrent.futures
import threading

class BaseLineAlgorithm2:
    def __init__(self, dados, nSimulation, budget, vehicles):
        self.graph = dados
        self.simulation_number = nSimulation
        self.buget_number = budget
        self.vehicles = vehicles

    def executar_algoritmo(self):
        
        # Criar janela e widget de texto para exibir os prints
        janela = tk.Tk()
        janela.title("Exemplo de Prints em Tempo Real")

        log_text = tk.Text(janela)
        log_text.pack()

        # Função para redirecionar os prints para o widget de texto
        def redirecionar_print(text):
            log_text.insert(tk.END, text + "\n")
            log_text.see(tk.END)

        # Redirecionar os prints para o widget de texto
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            print = redirecionar_print

            modifications = []
            arestas_criadas = []
            simulacoes = int(self.simulation_number)
            json_inicial = self.graph
            bestJson = json_inicial

            # Retorno da simulação da instância inicial
            simulador = SumoSimulation(self.graph, self.vehicles)
            BestAvgTravelTime = simulador.run_simulation()

            simulation_number = 1
            while simulacoes > 0:
                json_mod = copy.deepcopy(json_inicial)
                vertices = json_mod['vertices']
                coordenadas = json_mod['coordenadas']
                arestas = json_mod['arestas']
                current_modification = []
                budget = float(self.buget_number)
                
                while len(current_modification) < 2:
                    
                    if random.random() < 0.5:
                        json_mod, current_modification, budget = util.nova_lane(arestas, modifications, json_mod, current_modification, budget)
                    
                    else:
                        json_mod, current_modification, arestas_criadas, budget = util.nova_aresta(vertices, arestas, arestas_criadas, coordenadas, json_mod, current_modification, budget)
                
                # Decrementar variável de critério de parada caso essa combinação não tiver sido feita
                alternative_modification = [current_modification[1], current_modification[0]]
                if current_modification not in modifications and alternative_modification not in modifications:
                    modifications.append(current_modification)
                    simulacoes -= 1
                    print(f"Simulação # {simulation_number}")
                    print(f"Modificação: {current_modification}")
                    print("")
                    simulation_number += 1

                    # Simular modificação
                    simulador = SumoSimulation(json_mod, self.vehicles)
                    AvgTravelTime = simulador.run_simulation()

                    # Verificar se a modificação resultou em uma melhora
                    if AvgTravelTime < BestAvgTravelTime:
                        BestAvgTravelTime = AvgTravelTime
                        bestJson = json_mod

            # Printar a melhor melhora no final
            print(f"Modificações: {modifications}")
            print("")
            print(f'O melhor tempo de viagem foi: {BestAvgTravelTime}')

            # Gerar tela com as vias

            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Thread para o primeiro processo
                future1 = executor.submit(self.executar_processo, self.graph, log_text)

                # Thread para o segundo processo
                future2 = executor.submit(self.executar_processo, bestJson, log_text)

                # Aguardar a conclusão de ambos os processos
                concurrent.futures.wait([future1, future2])

                # Iniciar o mainloop em uma nova thread
                mainloop_thread = threading.Thread(target=janela.mainloop)
                mainloop_thread.start()

                # Aguardar a conclusão do mainloop
                mainloop_thread.join()

        return BestAvgTravelTime
    
    def call_simulations(self):
        
        sumo_path = shutil.which('sumo')
        sumo_dir = os.path.dirname(sumo_path)

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        sumoBinary = os.path.join(sumo_dir, "sumo-gui")
        sumoCmd = [sumoBinary, "-c", "src/sumo_data/config.sumocfg"]

        return sumoCmd

    def executar_processo(self, json_data, log_text):
        grafoFile = SumoFilesGenerator(json_data)
        grafoFile.generateSumoFile(file_name_edge="edges.xml", file_name_node="nodes.xml")

        subprocess.run(self.call_simulations())

