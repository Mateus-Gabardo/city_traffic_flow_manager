import random
import traci


class SumoVehicleRouter:
    def __init__(self, seed=None, min_speed=10, max_speed=30, accel=2, decel=4):
        self.seed = seed
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.accel = accel
        self.decel = decel

    def set_vehicle_routes(self, num_vehicles):
        if self.seed is not None:
            random.seed(self.seed)

        edges = traci.edge.getIDList()
        routes = []
        for i in range(num_vehicles):
            start_edge = random.choice(edges)
            end_edge = random.choice(edges)
            while end_edge == start_edge:
                end_edge = random.choice(edges)
            route = traci.simulation.findRoute(start_edge, end_edge)
            routes.append(route.edges)

        for i in range(num_vehicles):
            route_id = f"route_{i}"
            traci.route.add(route_id, routes[i])
            vehicle_id = f"vehicle_{i}"
            traci.vehicle.add(vehicle_id, route_id, depart=i, departSpeed="max",
                               typeID="passenger", minGap="0.5", maxSpeed=str(self.max_speed),
                               accel=str(self.accel), decel=str(self.decel))
