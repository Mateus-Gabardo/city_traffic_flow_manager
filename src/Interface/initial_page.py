import json
import tkinter as tk
from src.algorithms.baseline_algorithm import BaseLineAlgorithm


class initial_page:
    def __init__(self, master):
        self.master = master
        self.master.title('Home Page')

        # Define a largura e altura da janela
        self.largura = 500
        self.altura = 300

        # Obtém a largura e altura da tela
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()

        # Calcula a posição x e y da janela para ficar no centro da tela
        pos_x = int(largura_tela/2 - self.largura/2)
        pos_y = int(altura_tela/2 - self.altura/2)

        # Define a posição e tamanho da janela
        self.master.geometry(f"{self.largura}x{self.altura}+{pos_x}+{pos_y}")

        # Seletor de Instâncias
        self.instances = ['Instância 1', 'Instância 2']
        self.selected_instance = tk.StringVar()
        self.selected_instance.set(self.instances[0])
        self.instance_selector = tk.OptionMenu(self.master, self.selected_instance, *self.instances)
        self.instance_selector.pack(pady=10)

        # Seletor de Algoritmos de solução
        self.algorithms = ['Baseline']
        self.selected_algorithm = tk.StringVar()
        self.selected_algorithm.set(self.algorithms[0])
        self.algorithm_selector = tk.OptionMenu(self.master, self.selected_algorithm, *self.algorithms)
        self.algorithm_selector.pack(pady=10)

        # Parametros de entrada do Algoritmo escolhido
        self.simulation_label = tk.Label(self.master, text='Número de Simulações:')
        self.simulation_label.pack(pady=10)
        self.simulation_entry = tk.Entry(self.master)
        self.simulation_entry.pack(pady=10)

        # Botão de execução
        self.execute_button = tk.Button(self.master, text='Executar', command=self.execute_algorithm)
        self.execute_button.pack()

    def execute_algorithm(self):
        # Obtem a instância selecionada
        instance = self.selected_instance.get()

        # Obtem os dados da instância
        with open('src/data/grid/grid.json', 'r') as f:
            json_str = f.read()
            data = json.loads(json_str)

        # Executa o algoritmo selecionado
        algorithm = self.selected_algorithm.get()
        simulationNumber = self.simulation_entry.get()
        if algorithm == "Baseline":
            baseline = BaseLineAlgorithm(data, simulationNumber)
            avg_travel_time = baseline.executar_algoritmo()

        # Exibe os resultados
        self.results_page = ResultsPage(self.master, avg_travel_time)


class ResultsPage:
    def __init__(self, master, avg_travel_time):
        self.master = master
        self.master.title('Resultados')
        self.master.geometry('100x50')

        # Exibe os resultados
        self.result_label = tk.Label(self.master, text=f"Tempo médio de viagem: {avg_travel_time}")
        self.result_label.pack(pady=10)


#if __name__ == '__main__':
root = tk.Tk()
app = initial_page(root)
root.mainloop()