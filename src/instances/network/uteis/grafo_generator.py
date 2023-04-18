import json
import os

class GrafoGenerator:
    def __init__(self):
        self.grafo = {}

    def adicionar_aresta(self, u, v, atributos):
        if u not in self.grafo:
            self.grafo[u] = {}
        self.grafo[u][v] = atributos

    def salvar_grafo_em_arquivo(self, nome_arquivo, pasta_destino):
        # Concatenar o caminho da pasta destino com o nome do arquivo
        caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
        with open(caminho_arquivo, "w") as arquivo:
            json.dump(self.grafo, arquivo, indent=4)
        print("Grafo salvo em arquivo:", caminho_arquivo)