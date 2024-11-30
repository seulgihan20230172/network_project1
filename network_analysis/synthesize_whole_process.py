import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import random

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


# BA와 ER의 y값 공통 범위 계산
common_min = max(ba_avg_shortest_path.min(), er_avg_shortest_path.min())
common_max = min(ba_avg_shortest_path[2426], er_avg_shortest_path[2426])

# 공통 범위의 80% 설정
range_80_min = int(common_min + 0.1 * (common_max - common_min))
range_80_max = int(common_min + 0.9 * (common_max - common_min))

# range_80_min과 range_80_max를 정수로 변환
range_80_min = round(range_80_min)
range_80_max = round(range_80_max)

# 80% 범위에서 랜덤하게 custom_y 생성
custom_y = random.randint(range_80_min, range_80_max)

# 결과 출력
print(f"공통 범위: {common_min:.2f} - {common_max:.2f}")
print(f"80% 범위: {range_80_min:.2f} - {range_80_max:.2f}")
print(f"랜덤 custom_y: {custom_y:.2f}")

# custom_y 표시
plt.axhline(
    custom_y, color="red", linestyle="--", label=f"y = {custom_y}"
)  # y축 기준선 추가
plt.text(
    ba_edge_attack_number[0],  # 마지막 x값 근처
    custom_y,
    f"y = {custom_y}",
    color="red",
    fontsize=15,
    va="bottom",
    ha="right",
)

# BA 네트워크 x값 표시
for x, y in zip(ba_edge_attack_number, ba_avg_shortest_path):
    if np.isclose(y, custom_y, atol=0.1):  # BA y값에 맞는 custom_y
        plt.text(x, y - 100, f"{x}", color="blue", fontsize=15, ha="center")

# ER 네트워크 x값 표시
for x, y in zip(er_edge_attack_number, er_avg_shortest_path):
    if np.isclose(y, custom_y, atol=0.1):  # ER y값에 맞는 custom_y
        plt.text(x, y - 100, f"{x}", color="green", fontsize=15, ha="center")


# 그래프 라벨 및 제목
plt.xlabel("Edge Attack Number")
plt.ylabel("Average Shortest Path")
plt.title("Comparison of Average Shortest Path (BA vs ER Networks)")
plt.grid(True)
plt.legend()
plt.xlim(0, 2425)  # x축 범위 제한 추가

# 그래프 저장
combined_graph_path = os.path.join(
    output_combined_graph_dir, "combined_average_graph.png"
)
plt.savefig(combined_graph_path)
plt.close()

print(f"Combined graph saved at: {combined_graph_path}")
