from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import json

def create_data_model():
    # Read input from JSON file
    with open("level1a.json", 'r') as file:
        data = json.load(file)

    n_neighbourhoods = data['n_neighbourhoods']
    neighborhoods = data['neighbourhoods']
    start_point = data['restaurants']['r0']['restaurant_distance'][0]

    # Create distance matrix
    distance_matrix = [[0] * n_neighbourhoods for _ in range(n_neighbourhoods)]
    for i in range(n_neighbourhoods):
        for j in range(n_neighbourhoods):
            distance_matrix[i][j] = neighborhoods[f'n{i}']['distances'][j]

    data = {
        'distance_matrix': distance_matrix,
        'num_vehicles': 1,
        'depot': start_point,
        'vehicle_capacity': data['vehicles']['v0']['capacity']
    }
    return data

def tsp_optimization():
    # Instantiate the data problem
    data = create_data_model()

    # Create the routing index manager
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback
    def distance_callback(from_index, to_index):
        return data['distance_matrix'][manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Set vehicle capacity constraint
    capacity_dimension = 'Capacity'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        data['vehicle_capacity'],  # vehicle maximum capacity
        True,  # start cumul to zero
        capacity_dimension
    )
    capacity_dimension_index = routing.GetDimensionOrDie(capacity_dimension)

    # Setting first solution heuristic (cheapest addition)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console
    if solution:
        index = routing.Start(0)
        plan_output = {'start_point': f'n{manager.IndexToNode(index)}', 'path': [], 'total_distance': 0, 'vehicle': 'v0'}
        while not routing.IsEnd(index):
            plan_output['path'].append(f'n{manager.IndexToNode(index)}')
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            plan_output['total_distance'] += routing.GetArcCostForVehicle(previous_index, index, 0)
        plan_output['path'].append(f'n{manager.IndexToNode(index)}')  # Return to start point
        print(json.dumps(plan_output, indent=2))
    else:
        print('No solution found.')

if __name__ == '__main__':
    tsp_optimization()
