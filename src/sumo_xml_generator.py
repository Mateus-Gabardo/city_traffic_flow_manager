import json
import os

class SumoFilesGenerator:
    def __init__(self, json_str):
        self.graph = json.loads(json_str)

    def generate_nodes_file(self, filename, desteny):
        nosFile = os.path.join(desteny, filename)
        with open(nosFile, 'w') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<nodes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd">\n')
            for i, v in enumerate(self.graph['vertices']):
                f.write(f'   <node id="{v}" x="0.0" y="0.0" type="priority"/>\n')
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
    
    def generateSumoFile(self, file_name_node, file_name_edge, destiny = "src/instances"):
        self.generate_nodes_file(file_name_node, destiny)
        self.generate_edges_file(file_name_edge, destiny)