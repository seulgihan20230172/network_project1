import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 파일 경로 설정
network_dir = "repeat_num/DongER/ER_random_network/attack_results"  # 네트워크 파일들이 있는 폴더 경로
output_avg_graph_dir = "network_analysis/ER/Average_graph"  # 평균 그래프를 저장할 폴더

# 폴더 생성 (존재하지 않으면)
os.makedirs(output_avg_graph_dir, exist_ok=True)

# 네트워크 파일 리스트 (BA 네트워크 파일 경로)
ba_network_files = [f"{network_dir}/ER_network_{i}_paths.csv" for i in range(1, 11)]

# 모든 네트워크 데이터의 최대 길이 계산
max_length = 0
for file in ba_network_files:
    df = pd.read_csv(file)
    max_length = max(max_length, len(df))

# 평균 그래프 계산을 위한 초기화
avg_shortest_path = np.zeros(max_length)
count = np.zeros(max_length)  # 각 공격 단계별 데이터 수를 세기 위한 배열

# 각 네트워크 데이터를 누적하여 평균 계산
for file in ba_network_files:
    df = pd.read_csv(file)
    avg_shortest_path[: len(df)] += df["Average Shortest Path"].values
    count[: len(df)] += 1  # 데이터가 있는 부분에 대해 카운트

# 평균 계산
avg_shortest_path = avg_shortest_path / count  # 각 단계별 평균 계산

# Edge Attack Number 생성 (0부터 시작, max_length 크기)
edge_attack_number = np.arange(max_length)

# 평균 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(
    edge_attack_number,
    avg_shortest_path,
    marker="o",
    color="b",
    label="Average of ER Networks",
)
plt.xlabel("Edge Attack Number")
plt.ylabel("Average Shortest Path")
plt.title("Average Shortest Path vs Edge Attack Number (ER Networks)")
plt.grid(True)
plt.legend()

# 그래프 저장
avg_graph_path = os.path.join(
    output_avg_graph_dir, "average_shortest_path_vs_attack_number.png"
)
plt.savefig(avg_graph_path)
plt.close()

print(f"Average graph saved at: {avg_graph_path}")
