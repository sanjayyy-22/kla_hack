import json
import random

def read_input_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    n_neighbourhoods = data['n_neighbourhoods']
    neighborhoods = data['neighbourhoods']
    restaurants = data['restaurants']
    vehicles = data['vehicles']
    
    return n_neighbourhoods, neighborhoods, restaurants, vehicles

def create_distance_matrix(n_neighbourhoods, neighborhoods, restaurants):
    distances = []

    for i in range(n_neighbourhoods):
        if f'n{i}' not in neighborhoods:
            break
        distances.append(neighborhoods[f'n{i}']['distances'])

    return distances

def calculate_total_distance(path, distance_matrix):
    total_distance = sum(distance_matrix[i][j] for i, j in zip(path, path[1:]))
    total_distance += distance_matrix[path[-1]][path[0]]
    return total_distance

def nearest_neighbor(current, unvisited, distance_matrix):
    if not unvisited:
        return None

    return min(unvisited, key=lambda x: distance_matrix[int(current[1:])][x])


def solve_delivery_optimization(distance_matrix, neighborhoods, vehicles, capacity):
    n_neighbourhoods = len(distance_matrix)
    unvisited = set(range(n_neighbourhoods))  # All nodes
    paths = {f'v{i}': {} for i in range(5)}  # Updated to generate paths for v0, v1, v2, v3, v4
    
    for vehicle_id, vehicle_info in vehicles.items():
        unvisited_copy = unvisited.copy()
        current = vehicle_info['start_point']
        path_number = 1

        while unvisited_copy:
            current_capacity = 0
            path = [current]

            while current_capacity <= capacity:
                next_neighbour = nearest_neighbor(current, unvisited_copy, distance_matrix)
                if next_neighbour is not None:
                    if current_capacity + neighborhoods[f'n{next_neighbour}']['order_quantity'] <= capacity:
                        path.append(next_neighbour)
                        current_capacity += neighborhoods[f'n{next_neighbour}']['order_quantity']
                        unvisited_copy.remove(next_neighbour)
                    else:
                        break  # Move to the next path if adding the next neighbor exceeds capacity
                else:
                    break  # No more unvisited neighbors available
            
            paths[vehicle_id][f"path{path_number}"] = path
            path_number += 1

    return paths

def generate_output_path(paths):
    output = {}

    for vehicle_id, vehicle_paths in paths.items():
        vehicle_output = {}
        for path_key, path in vehicle_paths.items():
            vehicle_output[path_key] = [f'r0'] + [f'n{index}' for index in path] + [f'r0']
        
        output[vehicle_id] = vehicle_output

    return output

def write_output_to_json(output_data, output_json_file):
    with open(output_json_file, 'w') as file:
        json.dump(output_data, file, indent=2)

def main():
    # Read input from JSON file
    input_json_file = r"C:\21pw29\Student Handout\Input data\level2a.json" # Replace with the correct file path
    n_neighbourhoods, neighborhoods, restaurants, vehicles = read_input_from_json(input_json_file)

    # Create distance matrix
    distance_matrix = create_distance_matrix(n_neighbourhoods, neighborhoods, restaurants)

    # Solve delivery optimization problem
    paths = solve_delivery_optimization(distance_matrix, neighborhoods, vehicles=vehicles, capacity=250)  # Adjust capacity if needed

    # Generate output format
    output_data = generate_output_path(paths)
    output_json_file = "output_data2a.json"  # Replace with your desired output file name
    write_output_to_json(output_data, output_json_file)

    # Print output
    print(json.dumps(output_data, indent=2))

if __name__ == "__main__":
    main()
