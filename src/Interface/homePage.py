import tkinter as tk
#from src import main

def executarMain():
    main

window = tk.Tk()
largura = 500
altura = 500

# Obtem a largura e altura da tela
largura_tela = window.winfo_screenwidth()
altura_tela = window.winfo_screenheight()

# Calcula a posição x e y da janela para ficar no centro da tela
pos_x = int(largura_tela/2 - largura/2)
pos_y = int(altura_tela/2 - altura/2)

# Define a posição e tamanho da janela
window.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

#--------------------------------------------------------------------------------------------
# Seletor de Instâncias
instances = ['Instância 1', 'Instância 2']

intances_option = tk.StringVar()
intances_option.set(instances[0])

seletor_instances = tk.OptionMenu(window, intances_option, *instances, command=None)
seletor_instances.pack(pady=10)

# Seletro de Algoritmos de solução
algorithms = ['Baseline']

algorithms_option = tk.StringVar()
algorithms_option.set(algorithms[0])

seletor_algotirhms = tk.OptionMenu(window, algorithms_option, *algorithms, command=None)
seletor_algotirhms.pack(pady=10)

# Parametros de entrada do Algoritmo escolhido
vehicle_label = tk.StringVar()
vehicle_label.set('Número de Veículos:')

vehicle_entry = tk.Entry(window, textvariable=vehicle_label)
vehicle_entry.pack(pady=10)

# Botão de execução
btn_executar = tk.Button(window, text='Executar', command=None)
btn_executar.pack()

# Inicia o loop principal da interface gráfica que espera eventos do usuário
window.mainloop()