import json
import os

class GrafoJsonWriter:
    def __init__(self):
        self.vertices = []
        self.arestas = {}
        self.coordenadas = {}
        self.restricoes = {}

    def adicionar_aresta(self, v_origem, v_destino, dados):
        if v_origem not in self.vertices:
            self.vertices.append(v_origem)
        if v_destino not in self.vertices:
            self.vertices.append(v_destino)
        self.arestas[f"{v_origem}-{v_destino}"] = dados

    def salvar_arquivo_json(self, nome_arquivo, pasta_destino):
        grafo_json = {"vertices": self.vertices, "arestas": self.arestas, "coordenadas": self.coordenadas, "restricoes": self.restricoes}
        caminho_completo = os.path.join(pasta_destino, nome_arquivo)
        with open(caminho_completo, "w") as f:
            json.dump(grafo_json, f, indent=4)

    def adicionar_coordenadas(self, vertice, x, y):
        self.coordenadas[vertice] = {"x": x, "y": y}
        
    def adicionar_restricoes(self, restricoes):
        self.restricoes = restricoes