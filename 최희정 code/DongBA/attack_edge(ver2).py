import csv
import heapq
import random


def load_network(file_path):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        edges = [
            (int(source), int(target), float(weight))
            for source, target, weight in reader
        ]
    return edges


def calculate_average_shortest_path(n, edges):
    arr = [[float("inf")] * n for _ in range(n)]
    for s, e, cost in edges:
        arr[s][e] = cost

    total_distance = 0
    path_count = 0

    for start in range(n):
        dist_arr = [float("inf")] * n
        dist_arr[start] = 0
        q = []
        heapq.heappush(q, (0, start))

        while q:
            cur_dist, cur_pos = heapq.heappop(q)
            if dist_arr[cur_pos] < cur_dist:
                continue
            for next_pos in range(n):
                if arr[cur_pos][next_pos] != float("inf"):
                    next_dist = cur_dist + arr[cur_pos][next_pos]
                    if dist_arr[next_pos] > next_dist:
                        dist_arr[next_pos] = next_dist
                        heapq.heappush(q, (next_dist, next_pos))

        for end in range(n):
            if start != end:
                if dist_arr[end] == float("inf"):
                    # If any node is unreachable, return immediately
                    return float("inf")
                total_distance += dist_arr[end]
                path_count += 1

    return total_distance / path_count if path_count > 0 else float("inf")


def main():
    edges = load_network("er_network.csv")
    n = max(max(s, e) for s, e, _ in edges) + 1  # Determine number of nodes
    average_shortest_paths = []
    x = 0

    # Open a CSV file to write the results
    with open("paths.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Remaining Edges", "Average Shortest Path"])  # Write header

        while True:
            avg_path_length = calculate_average_shortest_path(n, edges)
            average_shortest_paths.append(avg_path_length)
            x = x + 1
            print(f"Average shortest path({x}): {avg_path_length}")

            # Write the current state to the CSV file
            writer.writerow([len(edges), avg_path_length])

            # Stop if no paths exist
            if avg_path_length == float("inf"):
                break

            # Randomly remove an edge
            if len(edges) > 1:
                edges.pop(random.randint(0, len(edges) - 1))
            else:
                break

    print(f"Final average shortest paths:", average_shortest_paths)


if __name__ == "__main__":
    main()
