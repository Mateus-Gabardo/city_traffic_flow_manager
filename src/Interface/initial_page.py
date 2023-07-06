import json
import csv
import tkinter as tk
from src.algorithms.baseline_algorithm import BaseLineAlgorithm
from src.algorithms.baseline_algorithm2 import BaseLineAlgorithm2
from src.algorithms.local_search_algorithm import LocalSearchAlgorithm


class initial_page:
    def __init__(self, master):
        self.master = master
        self.master.title('Home Page')

        # Define a largura e altura da janela
        self.largura = 1200
        self.altura = 300

        # Obtém a largura e altura da tela
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        # Calcula a posição x e y da janela para ficar no centro da tela
        pos_x = int(largura_tela/2 - self.largura/2)
        pos_y = int(altura_tela/2 - self.altura/2)

        # Define a posição e tamanho da janela
        self.master.geometry(f"{self.largura}x{self.altura}+{pos_x}+{pos_y}")

        self.data = None
        
        # Checkbox das Instâncias
        self.instances_label = tk.Label(self.master, text='Instâncias')
        self.instances_label.grid(row=0, column=0, padx=10, pady=2, sticky='w')

        self.instances = ['Grid 4x4', 'Sioux Falls']
        self.selected_instances = []
        self.instance_checkboxes = []
        for i, instance in enumerate(self.instances):
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.master, text=instance, variable=var)
            checkbox.grid(row=i+1, column=0, padx=10, pady=10, sticky='w')
            self.instance_checkboxes.append(checkbox)
            self.selected_instances.append(var)
        
        # Checkbox dos Algoritmos de solução
        self.algorithm_label = tk.Label(self.master, text='Algoritmos')
        self.algorithm_label.grid(row=0, column=1, padx=10, pady=2, sticky='w')

        self.algorithms = ['Baseline', 'Local Search', 'Iterated Local Search']
        self.selected_algorithms = []
        self.algorithm_checkboxes = []
        for i, algorithm in enumerate(self.algorithms):
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.master, text=algorithm, variable=var)
            checkbox.grid(row=i+1, column=1, padx=0, pady=10, sticky='w')
            self.algorithm_checkboxes.append(checkbox)
            self.selected_algorithms.append(var)

        # Estratégia de melhoria
        self.simulation_label_melhoria = tk.Label(self.master, text='Estratégia de melhoria')
        self.simulation_label_melhoria.grid(row=0, column=2, padx=10, pady=2, sticky='w')

        self.estrategia_melhoria = ['Melhor melhoria', 'Primeira melhoria']
        self.selected_melhoria = []
        self.melhoria_checkboxes = []
        for i, estrategia_melhoria in enumerate(self.estrategia_melhoria):
            var = tk.IntVar()
            checkbox = tk.Checkbutton(self.master, text=estrategia_melhoria, variable=var)
            checkbox.grid(row=i+1, column=2, padx=0, pady=10, sticky='w')
            self.melhoria_checkboxes.append(checkbox)
            self.selected_melhoria.append(var)

        # Número de simulações executadas
        self.simulation_label = tk.Label(self.master, text='Número de Simulações:')
        self.simulation_label.grid(row=4, column=0, padx=10, pady=2)
        self.simulation_entry = tk.Entry(self.master)
        self.simulation_entry.grid(row=4, column=1, padx=10, pady=10)
        # Quilometragem máxima (budget)
        self.simulation_label2 = tk.Label(self.master, text='Km Máximo(Budget):')
        self.simulation_label2.grid(row=4, column=2, padx=10, pady=2)
        self.simulation_entry2 = tk.Entry(self.master)
        self.simulation_entry2.grid(row=4, column=3, padx=10, pady=10)
        # Quantidade de Veículos
        self.vehicles_label = tk.Label(self.master, text='Quantidade de Veículos:')
        self.vehicles_label.grid(row=4, column=8, padx=4, pady=2)
        self.vehicles = tk.Entry(self.master)
        self.vehicles.grid(row=4, column=9, padx=5, pady=10)

        empty_label = tk.Label(self.master)
        empty_label.grid(row=4, column=0, columnspan=3, pady=10)

        # Botão de execução
        self.execute_button = tk.Button(self.master, text='Executar', command=self.execute_simulation)
        self.execute_button.grid(row=6, column=0, padx=10, pady=10)

    def execute_simulation(self):
        
        # Configurar arquivo CSV
        with open('src/sumo_data/resultados.csv', 'w', newline='') as arquivo_csv:
            writer = csv.writer(arquivo_csv)

            # Gravar o cabeçalho
            writer.writerow(['Instância', 'Algoritmo', 'Estratégia', 'Tempo de Execução', 'Simulações', 'Budget', 'Veículos'])

            simulationNumber = self.simulation_entry.get()
            budget = self.simulation_entry2.get()
            vehicles = self.vehicles.get()

            estrategias = []
            for i, var in enumerate(self.selected_melhoria):
                #melhoria = self.estrategia_melhoria[i]
                if var.get() == 1:
                    estrategias.append(i+1)
            # Verificar se os checkbuttons foram selecionados
            for i, var in enumerate(self.selected_instances):
                instance = self.instances[i]
                if var.get() == 1:
                    if instance == "Grid 4x4":
                        with open('src/data/grid/grid.json', 'r') as f:
                            json_str = f.read()
                            self.data = json.loads(json_str)

                    elif instance == "Sioux Falls":
                        with open('src/data/siouxFalls/siouxFalls.json', 'r') as f:
                            json_str = f.read()
                            self.data = json.loads(json_str)
    
                    for i, var in enumerate(self.selected_algorithms):
                        algorithm = self.algorithms[i]
                        if var.get() == 1:
                            if algorithm == "Local Search":
                                for estrategia in estrategias:
                                    avg_time = self.exec_algorithm(BaseLineAlgorithm2, LocalSearchAlgorithm, algorithm, budget, vehicles, estrategia, simulationNumber)
                                    # Gravar os resultados no arquivo CSV
                                    writer.writerow([instance, algorithm, estrategia, avg_time, simulationNumber, budget, vehicles])
                            else:
                                avg_time = self.exec_algorithm(BaseLineAlgorithm2, LocalSearchAlgorithm, algorithm, budget, vehicles, 0, simulationNumber)
                                # Gravar os resultados no arquivo CSV
                                writer.writerow([instance, algorithm, 0, avg_time, simulationNumber, budget, vehicles])

        # Exibe os resultados
        #self.results_page = ResultsPage(self.master, avg_travel_time)

    def exec_algorithm(self, BaseLineAlgorithm2, LocalSearchAlgorithm, algorithm, budget, vehicles, estrategia, simulationNumber):
        avg_travel_time = 0

        if algorithm == "Baseline":
            baseline = BaseLineAlgorithm2(self.data, simulationNumber, budget, vehicles)
            avg_travel_time = baseline.executar_algoritmo()

        elif algorithm == "Local Search":
            avg_travel_time = LocalSearchAlgorithm.localSearch(self.data, int(budget), int(simulationNumber), estrategia, int(vehicles))
        
        return avg_travel_time


class ResultsPage:
    def __init__(self, master, avg_travel_time):
        self.master = master
        self.master.title('Resultados')
        self.master.geometry('500x500')

        # Exibe os resultados
        self.result_label = tk.Label(self.master, text=f"Tempo médio de viagem: {avg_travel_time}")
        self.result_label.pack(pady=10)


root = tk.Tk()
app = initial_page(root)
root.mainloop()