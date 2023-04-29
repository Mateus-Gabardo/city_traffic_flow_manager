import re
import xml.etree.ElementTree as ET

class SumoXMLRouterGenerator:
    def __init__(self, demands_path, edge_info_path, output_file_path):
        self.demands_path = demands_path
        self.edge_info_path = edge_info_path
        self.output_file_path = output_file_path
    
    def extract_demands(self):
        demands = {}
        with open(self.demands_path) as file:
            origin = None
            for line in file:
                line = line.strip()
                if line.startswith("Origin"):
                    origin = int(line.split()[1])
                    demands[origin] = {}
                elif origin is not None:
                    match = re.match(r"(\d+)\s:\s(-?\d+\.\d+)\s*(?:;|$)", line)
                    if match:
                        edge_id = match.group(1)
                        demand = float(match.group(2))
                        if demand != 0:
                            demands[origin].setdefault(edge_id, []).append(demand)
        return demands

    def extract_edge_info(self):
        edge_info = {}
        tree = ET.parse(self.edge_info_path)
        root = tree.getroot()

        for edge in root.iter('edge'):
            edge_id = edge.get('id')
            edge_info[edge_id] = {
                'numLanes': int(edge.get('numLanes')),
                'speed': float(edge.get('speed')),
                'length': float(edge.get('length', '0')),
                'depart': edge.get('depart', '0')
            }

        return edge_info

    def generate_custom_sumo_routes_file(self):
        demands = self.extract_demands()
        edge_info = self.extract_edge_info()
        root = ET.Element('routes')
        for origin, edges in demands.items():
            for edge_id, values in edges.items():
                for i in range(len(values)):
                    vehicle_elem = ET.SubElement(root, 'vehicle', {'id': f'vehicle_{origin}_{edge_id}_{i}', 'depart': '0', 'route': f'{edge_id}', 'color': '1,0,0'})
                    route_elem = ET.SubElement(vehicle_elem, 'route', {'edges': f'{edge_id}', 'numLanes': str(edge_info[edge_id]["numLanes"]), 'speed': str(edge_info[edge_id]["speed"])})
                    route_elem.set("length", str(edge_info[edge_id]["length"]))

        tree = ET.ElementTree(root)
        tree.write(self.output_file_path, encoding='UTF-8', xml_declaration=True)

