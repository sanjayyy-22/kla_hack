import json
import networkx as nx

def create_graph(data):
    """Create a graph using NetworkX."""
    G = nx.Graph()

    # Add neighbourhood nodes
    for n_id, n_data in data['neighbourhoods'].items():
        G.add_node(n_id)

    # Add restaurant node
    G.add_node("r0")

    # Add edges and distances
    for n_id, n_data in data['neighbourhoods'].items():
        G.add_edge("r0", n_id, weight=data['restaurants']['r0']['neighbourhood_distance'][int(n_id[1:])])
        G.add_edge(n_id, "r0", weight=data['restaurants']['r0']['neighbourhood_distance'][int(n_id[1:])])

    return G

def find_paths(G, start_node, capacity):
    """Find paths for the scooter using a simple algorithm."""
    paths = []
    visited_nodes = set()

    for path_num, path_nodes in data['vehicles']['v0'].items():
        current_path = [start_node]
        current_capacity = 0

        for node in path_nodes:
            if node not in visited_nodes:
                visited_nodes.add(node)
                current_path.append(node)
                current_capacity += data['neighbourhoods'][node[1:]]['order_quantity']

                if current_capacity > capacity:
                    break

        current_path.append(start_node)
        paths.append(current_path)

    return paths

if __name__ == "__main__":
    with open('level1a.json') as file:
        data = json.load(file)

    graph = create_graph(data)
    scooter_paths = find_paths(graph, "r0", data['vehicles']['v0']['capacity'])

    output_dict = {"v0": {}}
    for i, path in enumerate(scooter_paths, start=1):
        output_dict["v0"]["path{}".format(i)] = path

    print(json.dumps(output_dict, indent=2))
