import json
import numpy as np

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

    return min(unvisited, key=lambda x: distance_matrix[current][x])

def solve_delivery_optimization(distance_matrix, capacity, neighborhoods):
    n_neighbourhoods = len(distance_matrix)
    unvisited = set(range(n_neighbourhoods))  # All nodes
    paths = []

    while unvisited:
        current = unvisited.pop()
        path = [current]
        current_capacity = neighborhoods[f'n{current}']['order_quantity']  # Initialize current capacity

        while current_capacity <= capacity:
            next_neighbour = nearest_neighbor(current, unvisited, distance_matrix)
            if next_neighbour is not None:
                if current_capacity + neighborhoods[f'n{next_neighbour}']['order_quantity'] <= capacity:
                    path.append(next_neighbour)
                    current_capacity += neighborhoods[f'n{next_neighbour}']['order_quantity']
                    unvisited.remove(next_neighbour)
                else:
                    break  # Move to the next path if adding the next neighbor exceeds capacity
            else:
                break  # No more unvisited neighbors available

        paths.append(path)

    return paths


def generate_output_path(paths, start_point, distance_matrix):
    output = {"v0": {}}
    
    for idx, path in enumerate(paths, start=1):
        path_key = f"path{idx}"
        output["v0"][path_key] = [start_point] + [f'n{index}' for index in path] + [start_point]
        # output["v0"][path_key] = calculate_total_distance(path, distance_matrix)  # Corrected this line

    return output

def write_output_to_json(output_data, output_json_file):
    with open(output_json_file, 'w') as file:
        json.dump(output_data, file, indent=2)

def main():
    # Read input from JSON file
    input_json_file = r"C:\Users\Sanjay\Documents\Placement\21pw29\Student Handout\Input data\level1a.json"
    n_neighbourhoods, neighborhoods, restaurants, vehicles = read_input_from_json(input_json_file)
    capacity = vehicles['v0']['capacity']

    # Create distance matrix
    distance_matrix = create_distance_matrix(n_neighbourhoods, neighborhoods, restaurants)

    # Solve delivery optimization problem
    paths = solve_delivery_optimization(distance_matrix, capacity, neighborhoods)

    # Generate output format
    output_data = generate_output_path(paths, vehicles['v0']['start_point'], distance_matrix)
    output_json_file = "your_output1b.json"  # Replace with your desired output file name
    write_output_to_json(output_data, output_json_file)

    # Print output
    print(json.dumps(output_data, indent=2))

if __name__ == "__main__":
    main()
