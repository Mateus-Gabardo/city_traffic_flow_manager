import random
import traci

# Classe utilitária para adicionar veículos no grafo
class VehicleIntroducer:
    def __init__(self, seed, vehicle_info, route_info):
        self.seed = seed
        self.vehicle_info = vehicle_info
        self.route_info = route_info

    def introduce_vehicles(self):
        random.seed(self.seed)
        for i, vehicle in enumerate(self.vehicle_info):
            vehicle_id = f"vehicle{i}"
            route_id = vehicle["route_id"]
            depart_time = vehicle["depart_time"]
            traci.vehicle.add(vehicle_id, route_id, depart=depart_time)


# Exemplo de chamada do método introduce_vehicles()

# Dados de veículos
vehicle_info = [
    {"route_id": "route1", "depart_time": 0},
    {"route_id": "route2", "depart_time": 10},
    {"route_id": "route3", "depart_time": 20}
]

# Dados de rotas
route_info = {
    "route1": ["edge1", "edge2", "edge3"],
    "route2": ["edge4", "edge5", "edge6"],
    "route3": ["edge7", "edge8", "edge9"]
}

# Criação de uma instância da classe VehicleIntroducer
vehicle_introducer = VehicleIntroducer(seed=1234, vehicle_info=vehicle_info, route_info=route_info)

# Chamada do método introduce_vehicles()
vehicle_introducer.introduce_vehicles()