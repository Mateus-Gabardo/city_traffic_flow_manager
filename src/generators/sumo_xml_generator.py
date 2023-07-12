import os
import subprocess

class SumoFilesGenerator:
    def __init__(self, json_str):
        self.graph = json_str

    def generate_nodes_file(self, filename, desteny):
        nosFile = os.path.join(desteny, filename)
        with open(nosFile, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">\n')
            for i, v in enumerate(self.graph['vertices']):
                eixo = self.graph['coordenadas']
                x = eixo[v]['x']
                y = eixo[v]['y']
                f.write(f'   <node id="{v}" x="{x}" y="{y}" type="priority"/>\n')
            f.write('</nodes>')

    def generate_edges_file(self, filename, desteny):
        edgesFile = os.path.join(desteny, filename)
        with open(edgesFile, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<edges xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd">\n')
            for k, v in self.graph['arestas'].items():
                src, dst = k.split('-')
                f.write(f'   <edge id="{k}" from="{src}" to="{dst}" priority="{v["priority"]}" numLanes="{v["numLanes"]}" speed="{v["maxSpeed"]}" />\n')
            f.write('</edges>')
    
    def generate_net_file(self, desteny, filename, nodeFile, edgeFile):
        nodes_file = os.path.join(desteny, nodeFile)
        edges_file = os.path.join(desteny, edgeFile)
        net_file = os.path.join(desteny, filename)
        subprocess.run(["netconvert", "--node-files", nodes_file, "--edge-files", edges_file, "-o", net_file, "--no-warnings"])
    
    def generateSumoFile(self, file_name_node, file_name_edge, destiny = "src/sumo_data"):
        self.generate_nodes_file(file_name_node, destiny)
        self.generate_edges_file(file_name_edge, destiny)
        self.generate_net_file(destiny, "network.net.xml", file_name_node, file_name_edge)