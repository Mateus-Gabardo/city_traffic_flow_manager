import re
import xml.etree.ElementTree as ET

def extract_demands(file_path):
    demands = {}
    with open(file_path) as file:
        origin = None
        for line in file:
            line = line.strip()
            if line.startswith("Origin"):
                origin = int(line.split()[1])
                demands[origin] = {}
            elif origin is not None:
                match = re.match(r"([A-Z])\s:\s(-?\d+\.\d+);?", line)
                if match:
                    edge_id = match.group(1)
                    demand = float(match.group(2))
                    if demand != 0:
                        demands[origin].setdefault(edge_id, []).append(demand)
    return demands

def extract_edge_info(edge_file_path):
    edge_info = {}
    tree = ET.parse(edge_file_path)
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

def generate_custom_sumo_routes_file(demands, edge_info, output_file):
    root = ET.Element('routes')
    for origin, edges in demands.items():
        for edge_id, values in edges.items():
            for i in range(len(values)):
                vehicle_elem = ET.SubElement(root, 'vehicle', {'id': f'vehicle_{origin}_{edge_id}_{i}', 'depart': '0', 'route': f'{edge_id}', 'color': '1,0,0'})
                route_elem = ET.SubElement(vehicle_elem, 'route', {'edges': f'{edge_id}'})
    
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)

demands = extract_demands('data/exemplo/trips.tntp')
edge_info = extract_edge_info('instances/edges.xml')
generate_custom_sumo_routes_file(demands, edge_info, 'custom_sumo_routes.xml')

