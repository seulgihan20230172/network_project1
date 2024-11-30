import heapq
import random
from multiprocessing import Pool, cpu_count
import csv
import time

def load_network(file_path):
    """Load network data from CSV file."""
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        edges = [
            (int(source), int(target), float(weight))
            for source, target, weight in reader
        ]
    return edges

def dijkstra(n, graph, start):
    """Single-source shortest path using Dijkstra's algorithm."""
    distances = [float("inf")] * n
    distances[start] = 0
    queue = [(0, start)]  # (distance, node)

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    return distances

def calculate_for_one_node(args):
    """Helper function to calculate shortest paths for one node."""
    n, graph, start = args
    distances = dijkstra(n, graph, start)
    total_distance = sum(d for d in distances if d < float("inf"))
    reachable_nodes = sum(1 for d in distances if d < float("inf") and d > 0)
    return total_distance, reachable_nodes

def calculate_average_shortest_path_parallel(n, graph):
    """Calculate the average shortest path in parallel."""
    with Pool(cpu_count()) as pool:
        results = pool.map(calculate_for_one_node, [(n, graph, i) for i in range(n)])
    
    total_distance = sum(res[0] for res in results)
    total_paths = sum(res[1] for res in results)
    return total_distance / total_paths if total_paths > 0 else float("inf")

def remove_random_edge(edges, graph):
    """Remove a random edge from the graph."""
    if edges:
        # Remove a random edge
        removed_edge = edges.pop(random.randint(0, len(edges) - 1))
        s, e, _ = removed_edge
        # Remove edge from adjacency list
        graph[s] = [(neighbor, weight) for neighbor, weight in graph[s] if neighbor != e]
    return edges, graph

def main():
    edges = load_network("ER_network_1.csv")
    n = max(max(s, e) for s, e, _ in edges) + 1

    # Build adjacency list
    graph = [[] for _ in range(n)]
    for s, e, weight in edges:
        graph[s].append((e, weight))

    start_time = time.time()

    with open("average_shortest_paths_with_removals.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Remaining Edges", "Average Shortest Path"])
        
        while edges:
            # Calculate the average shortest path
            avg_path_length = calculate_average_shortest_path_parallel(n, graph)
            print(f"Remaining edges: {len(edges)}, Average shortest path: {avg_path_length}")

            # Write to CSV
            writer.writerow([len(edges), avg_path_length])

            # Stop if graph is disconnected (infinite shortest path)
            if avg_path_length == float("inf"):
                break

            # Remove a random edge
            edges, graph = remove_random_edge(edges, graph)

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
