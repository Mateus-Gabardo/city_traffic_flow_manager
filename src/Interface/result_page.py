import tkinter as tk

def exibir_log(text):
    log_text.insert(tk.END, text + "\n")
    log_text.see(tk.END)  # Rolar automaticamente para a última linha adicionada

# Criação da janela principal
janela = tk.Tk()
janela.title("Simulação")

# imagem do grafo
#imagem = tk.PhotoImage(file="caminho_da_imagem.png") 
#imagem_label = tk.Label(janela, image=imagem)
#imagem_label.pack()

# Criação do log
log_frame = tk.Frame(janela)
log_frame.pack(pady=10)

log_label = tk.Label(log_frame, text="Log da Simulação")
log_label.pack()

log_text = tk.Text(log_frame, height=10, width=50)
log_text.pack()

# Exemplo de adição de texto ao log
exibir_log("Iniciando simulação...")
exibir_log("Passo 1 concluído.")
exibir_log("Passo 2 concluído.")

# Iniciar a execução da interface gráfica
janela.mainloop()