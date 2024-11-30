import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 파일 경로 설정
ba_network_dir = "repeat_num/DongBA/BA_random_network/attack_results"
er_network_dir = "repeat_num/DongER/ER_random_network/attack_results"
output_combined_graph_dir = "network_analysis/synthesize"

# 폴더 생성
os.makedirs(output_combined_graph_dir, exist_ok=True)

# BA 및 ER 네트워크 파일 리스트
ba_network_files = [f"{ba_network_dir}/BA_network_{i}_paths.csv" for i in range(1, 11)]
er_network_files = [f"{er_network_dir}/ER_network_{i}_paths.csv" for i in range(1, 11)]


# 평균 그래프 계산 함수
def calculate_average_graph(network_files):
    max_length = 0
    for file in network_files:
        df = pd.read_csv(file)
        max_length = max(max_length, len(df))

    avg_shortest_path = np.zeros(max_length)
    count = np.zeros(max_length)

    for file in network_files:
        df = pd.read_csv(file)
        avg_shortest_path[: len(df)] += df["Average Shortest Path"].values
        count[: len(df)] += 1

    avg_shortest_path = avg_shortest_path / count  # 평균 계산
    edge_attack_number = np.arange(max_length)  # Edge Attack Number 생성
    return edge_attack_number, avg_shortest_path


# BA와 ER 평균 그래프 데이터 계산
ba_edge_attack_number, ba_avg_shortest_path = calculate_average_graph(ba_network_files)
er_edge_attack_number, er_avg_shortest_path = calculate_average_graph(er_network_files)

# 그래프 그리기
plt.figure(figsize=(12, 8))

# BA 네트워크 평균 그래프
plt.plot(
    ba_edge_attack_number,
    ba_avg_shortest_path,
    marker="o",
    color="blue",
    label="Average of BA Networks",
)

# ER 네트워크 평균 그래프
plt.plot(
    er_edge_attack_number,
    er_avg_shortest_path,
    marker="o",
    color="green",
    label="Average of ER Networks",
)

# y값 범위 확인
print("BA y값 범위:", ba_avg_shortest_path.min(), "-", ba_avg_shortest_path[-2])
print("ER y값 범위:", er_avg_shortest_path.min(), "-", er_avg_shortest_path[-2])

# 적절한 custom_y 설정 (예: 3)
custom_y = 1500

# custom_y 표시
plt.axhline(
    custom_y, color="red", linestyle="--", label=f"y = {custom_y}"
)  # y축 기준선 추가
plt.text(
    ba_edge_attack_number[0],  # 마지막 x값 근처
    custom_y,
    f"y = {custom_y}",
    color="red",
    fontsize=10,
    va="bottom",
    ha="right",
)

# BA 네트워크 x값 표시
for x, y in zip(ba_edge_attack_number, ba_avg_shortest_path):
    if np.isclose(y, custom_y, atol=0.2):  # BA y값에 맞는 custom_y
        plt.text(x, y - 100, f"{x}", color="blue", fontsize=8, ha="center")

# ER 네트워크 x값 표시
for x, y in zip(er_edge_attack_number, er_avg_shortest_path):
    if np.isclose(y, custom_y, atol=0.2):  # ER y값에 맞는 custom_y
        plt.text(x, y - 100, f"{x}", color="green", fontsize=8, ha="center")


# 그래프 라벨 및 제목
plt.xlabel("Edge Attack Number")
plt.ylabel("Average Shortest Path")
plt.title("Comparison of Average Shortest Path (BA vs ER Networks)")
plt.grid(True)
plt.legend()

# 그래프 저장
combined_graph_path = os.path.join(
    output_combined_graph_dir, "combined_average_graph.png"
)
plt.savefig(combined_graph_path)
plt.close()

print(f"Combined graph saved at: {combined_graph_path}")
