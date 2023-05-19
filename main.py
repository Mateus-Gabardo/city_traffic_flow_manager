from src.algorithms.baseline_algorithm import BaseLineAlgorithm
from src.Interface.initial_page import initial_page
import tkinter as tk

def main():
    root = tk.Tk()
    tela = initial_page(root)
    root.mainloop()

main()