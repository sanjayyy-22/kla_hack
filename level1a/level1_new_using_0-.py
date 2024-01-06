# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 13:38:43 2024

@author: 21pw29
"""

import json

def read_input_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    n_neighbourhoods = data['n_neighbourhoods']
    neighborhoods = data['neighbourhoods']
    restaurants = data['restaurants']
    
    return n_neighbourhoods, neighborhoods, restaurants

def create_distance_matrix(n_neighbourhoods, neighborhoods, restaurants):
    distances = []

    for i in range(n_neighbourhoods):
        if f'n{i}' not in neighborhoods:
            break
        distances.append(neighborhoods[f'n{i}']['distances'])

    return distances

def calculate_total_distance(path, distance_matrix):
    return sum(distance_matrix[i][j] for i, j in zip(path, path[1:])) + distance_matrix[path[-1]][path[0]]

def solve_tsp_nearest_neighbor(distance_matrix):
    n_neighbourhoods = len(distance_matrix)
    unvisited = set(range(1, n_neighbourhoods))  # All nodes except the starting node
    path = [0]  # Start from the first neighborhood
    total_distance = 0

    for _ in range(n_neighbourhoods - 1):
        current = path[-1]
        next_neighbour = min(unvisited, key=lambda x: distance_matrix[current][x])
        path.append(next_neighbour)
        unvisited.remove(next_neighbour)
        total_distance += distance_matrix[current][next_neighbour]

    path.append(path[0])  # Return to the starting point
    return path, total_distance

def generate_output_path(path, start_point):
    return {"v0": {"path": [start_point] + [f'n{index}' for index in path[1:]] + [start_point]}}

def write_output_to_json(output_data, output_json_file):
    with open(output_json_file, 'w') as file:
        json.dump(output_data, file, indent=2)

def main():
    # Read input from JSON file
    input_json_file = r"C:\Users\Sanjay\Documents\Placement\21pw29\Student Handout\Input data\level1a.json"  # Replace with your input file name
    n_neighbourhoods, neighborhoods, restaurants = read_input_from_json(input_json_file)

    # Create distance matrix
    distance_matrix = create_distance_matrix(n_neighbourhoods, neighborhoods, restaurants)

    # Solve TSP using nearest neighbor algorithm
    shortest_path, total_distance = solve_tsp_nearest_neighbor(distance_matrix)

    # Generate output format
    output_data = generate_output_path(shortest_path, "r0")
    output_json_file = "your_output.json"  # Replace with your desired output file name
    write_output_to_json(output_data, output_json_file)

    # Print output
    print(json.dumps(output_data, indent=2))

if __name__ == "__main__":
    main()
