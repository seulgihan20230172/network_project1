import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 파일 경로 설정
network_dir = "repeat_num/DongBA/BA_random_network/attack_results"  # 네트워크 파일들이 있는 폴더 경로
output_graph_dir = "network_analysis/graph"  # 그래프를 저장할 폴더
output_derivative_dir = "network_analysis/Derivative_graph"  # 기울기를 저장할 폴더
output_dd_derivative_dir = "network_analysis/D_Derivative_graph"  # 두 번째 미분을 저장할 폴더
final_remaining_edges_file = "network_analysis/final_remaining_edges.csv"  # 마지막 remaining edges를 저장할 파일

# 폴더 생성 (존재하지 않으면)
os.makedirs(output_graph_dir, exist_ok=True)
os.makedirs(output_derivative_dir, exist_ok=True)
os.makedirs(output_dd_derivative_dir, exist_ok=True)

# 마지막 remaining edges를 저장할 리스트
final_remaining_edges = []

# 네트워크 파일 리스트
network_files = [f"{network_dir}/BA_network_{i}_paths.csv" for i in range(1, 11)]

# 각 네트워크에 대해 작업 시작
for network_file in network_files:
    # CSV 파일 읽기
    df = pd.read_csv(network_file)
    
    # "Remaining Edges"와 "Average Shortest Path" 열 가져오기
    remaining_edges = df["Remaining Edges"].values
    avg_shortest_path = df["Average Shortest Path"].values

    # 1. 평균 최단 거리 그래프 그리기
    plt.figure(figsize=(10, 6))
    plt.plot(remaining_edges, avg_shortest_path, marker='o', color='b', label="Average Shortest Path")
    plt.xlabel("Remaining Edges")
    plt.ylabel("Average Shortest Path")
    plt.title(f"Network {network_file.split('/')[-1]}: Average Shortest Path vs Remaining Edges")
    plt.grid(True)
    plt.legend()

    # 그래프 저장
    graph_file_path = os.path.join(output_graph_dir, f"{network_file.split('/')[-1].split('.')[0]}_graph.png")
    plt.savefig(graph_file_path)
    plt.close()

    # 2. 평균 최단 거리의 기울기 (미분) 계산
    diff_avg_shortest_path = np.diff(avg_shortest_path)  # 첫 번째 미분
    diff_remaining_edges = np.diff(remaining_edges)  # 첫 번째 미분
    derivative = diff_avg_shortest_path / diff_remaining_edges  # 기울기

    # 첫 번째 미분 그래프 (Derivative)
    sampling_step = 10  # 샘플링 간격 설정
    sampled_edges = remaining_edges[:-1][::sampling_step]  # remaining_edges에서 10개 간격으로 샘플링
    sampled_derivative = derivative[::sampling_step]  # derivative도 동일 간격으로 샘플링

    plt.figure(figsize=(10, 6))
    plt.plot(sampled_edges, sampled_derivative, color='r', label="Derivative of Average Shortest Path")
    plt.xlabel("Remaining Edges")
    plt.ylabel("Derivative of Average Shortest Path")
    plt.title(f"Network {network_file.split('/')[-1]}: Derivative of Average Shortest Path")
    plt.ylim(-2, 2)  # y축 범위 제한
    plt.grid(True)
    plt.legend()

    # 그래프 저장
    derivative_graph_file_path = os.path.join(output_derivative_dir, f"{network_file.split('/')[-1].split('.')[0]}_derivative.png")
    plt.savefig(derivative_graph_file_path)
    plt.close()


    # 3. 두 번째 미분 (변화율) 계산
    second_derivative = np.diff(derivative) / np.diff(remaining_edges[:-1])  # 두 번째 미분

    # 두 번째 미분 그래프 (Second Derivative)
    sampling_step = 10  # 샘플링 간격 설정
    sampled_edges_2nd = remaining_edges[:-2][::sampling_step]  # remaining_edges에서 10개 간격으로 샘플링
    sampled_second_derivative = second_derivative[::sampling_step]  # 두 번째 미분도 동일 간격으로 샘플링

    plt.figure(figsize=(10, 6))
    plt.plot(sampled_edges_2nd, sampled_second_derivative, color='g', label="Second Derivative of Average Shortest Path")
    plt.xlabel("Remaining Edges")
    plt.ylabel("Second Derivative of Average Shortest Path")
    plt.title(f"Network {network_file.split('/')[-1]}: Second Derivative of Average Shortest Path")
    plt.ylim(-2, 2)  # y축 범위 제한
    plt.grid(True)
    plt.legend()

    # 그래프 저장
    dd_derivative_graph_file_path = os.path.join(output_dd_derivative_dir, f"{network_file.split('/')[-1].split('.')[0]}_dd_derivative.png")
    plt.savefig(dd_derivative_graph_file_path)
    plt.close()


    # 4. 마지막 remaining edges 값 저장
    final_remaining_edges.append({
        'Network': network_file.split('/')[-1],
        'Last Remaining Edges': remaining_edges[-1]
    })

# 마지막 remaining edges 값을 CSV로 저장
final_remaining_edges_df = pd.DataFrame(final_remaining_edges)
final_remaining_edges_df.to_csv(final_remaining_edges_file, index=False)

print("remaining_edges:", remaining_edges)
print("len(remaining_edges):", len(remaining_edges))
print("len(derivative):", len(derivative))  # 첫 번째 미분 결과
print("len(second_derivative):", len(second_derivative))  # 두 번째 미분 결과

print("remaining_edges (x축 for Derivative):", remaining_edges[:-1])
print("Derivative values (y축):", derivative)

print("remaining_edges (x축 for Second Derivative):", remaining_edges[:-2])
print("Second Derivative values (y축):", second_derivative)

print("Derivative max:", np.max(derivative), "min:", np.min(derivative))
print("Second Derivative max:", np.max(second_derivative), "min:", np.min(second_derivative))


print("File saved.")
