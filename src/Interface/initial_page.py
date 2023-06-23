import json
import tkinter as tk
from src.algorithms.baseline_algorithm import BaseLineAlgorithm
from src.algorithms.baseline_algorithm2 import BaseLineAlgorithm2
from src.algorithms.local_search_algorithm import LocalSearchAlgorithm


class initial_page:
    def __init__(self, master):
        self.master = master
        self.master.title('Home Page')

        # Define a largura e altura da janela
        self.largura = 500
        self.altura = 500

        # Obtém a largura e altura da tela
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        # Calcula a posição x e y da janela para ficar no centro da tela
        pos_x = int(largura_tela/2 - self.largura/2)
        pos_y = int(altura_tela/2 - self.altura/2)

        # Define a posição e tamanho da janela
        self.master.geometry(f"{self.largura}x{self.altura}+{pos_x}+{pos_y}")

        # Seletor de Instâncias
        self.data = None
        self.instances = ['Grid 4x4', 'Sioux Falls']
        self.selected_instance = tk.StringVar()
        self.selected_instance.set(self.instances[0])
        self.instance_selector = tk.OptionMenu(self.master, self.selected_instance, *self.instances)
        self.instance_selector.pack(pady=10)

        # Seletor de Algoritmos de solução
        self.algorithms = ['Baseline','Baseline2','Local Search','Iterated Local Search']
        self.selected_algorithm = tk.StringVar()
        self.selected_algorithm.set(self.algorithms[0])
        self.algorithm_selector = tk.OptionMenu(self.master, self.selected_algorithm, *self.algorithms)
        self.algorithm_selector.pack(pady=10)

        # Estratégia de melhoria
        self.simulation_label_melhoria = tk.Label(self.master, text='Estratégia de melhoria')
        self.simulation_label_melhoria.pack(pady=2)
        self.estrategia_melhoria = ['Primeira melhoria','Melhor melhoria']
        self.selected_estrategia = tk.StringVar()
        self.selected_estrategia.set(self.estrategia_melhoria[0])
        self.estrategia_selector = tk.OptionMenu(self.master, self.selected_estrategia, *self.estrategia_melhoria)
        self.estrategia_selector.pack(pady=10)

        # Número de simulações executadas
        self.simulation_label = tk.Label(self.master, text='Número de Simulações:')
        self.simulation_label.pack(pady=2)
        self.simulation_entry = tk.Entry(self.master)
        self.simulation_entry.pack(pady=10)

        # Quilometragem máxima (budget)
        self.simulation_label2 = tk.Label(self.master, text='Km Máximo(Budget):')
        self.simulation_label2.pack(pady=2)
        self.simulation_entry2 = tk.Entry(self.master)
        self.simulation_entry2.pack(pady=10)

        # Botão de execução
        self.execute_button = tk.Button(self.master, text='Executar', command=self.execute_algorithm)
        self.execute_button.pack()

    def execute_algorithm(self):
        # Obtem a instância selecionada
        instance = self.selected_instance.get()
        if instance == "Grid 4x4":
            with open('src/data/grid/grid.json', 'r') as f:
                json_str = f.read()
                self.data = json.loads(json_str)
        elif instance == "Sioux Falls":
            with open('src/data/siouxFalls/siouxFalls.json', 'r') as f:
                json_str = f.read()
                self.data = json.loads(json_str)

        # Executa o algoritmo selecionado
        algorithm = self.selected_algorithm.get()
        simulationNumber = self.simulation_entry.get()
        budget = self.simulation_entry2.get()
        estrategia = self.selected_estrategia.get()
        if(estrategia == 'Primeira melhoria'):
            estrategia = 2
        else:
            estrategia = 1

        if algorithm == "Baseline":
            baseline = BaseLineAlgorithm(self.data, simulationNumber, budget)
            avg_travel_time = baseline.executar_algoritmo()
        
        if algorithm == "Baseline2":
            baseline = BaseLineAlgorithm2(self.data, simulationNumber, budget)
            avg_travel_time = baseline.executar_algoritmo()

        if algorithm == "Local Search":
            avg_travel_time = LocalSearchAlgorithm.localSearch(self.data, int(budget), int(simulationNumber), estrategia)

        # Exibe os resultados
        # self.results_page = ResultsPage(self.master, avg_travel_time)


# class ResultsPage:
#     def __init__(self, master, avg_travel_time):
#         self.master = master
#         self.master.title('Resultados')
#         self.master.geometry('500x500')

#         # Exibe os resultados
#         self.result_label = tk.Label(self.master, text=f"Tempo médio de viagem: {avg_travel_time}")
#         self.result_label.pack(pady=10)


root = tk.Tk()
app = initial_page(root)
root.mainloop()