import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 파일 경로 설정
network_dir = "repeat_num/DongBA_result/DongBA//BA_random_network_results"  # 네트워크 파일들이 있는 폴더 경로
output_graph_dir = "network_analysis/BA"  # 평균 그래프를 저장할 폴더
os.makedirs(output_graph_dir, exist_ok=True)

# 네트워크 파일 리스트
network_files = [
    f"{network_dir}/BA_network_{i}_average_shortest_paths.csv" for i in range(1, 51)
]

# 데이터를 저장할 리스트
all_avg_shortest_paths = []

# 각 네트워크의 데이터를 수집
for network_file in network_files:
    df = pd.read_csv(network_file)

    # `Average Shortest Path`에서 `inf` 값 확인
    if np.isinf(df["Average Shortest Path"]).any():
        print(f"Skipping {network_file} due to 'inf' values.")
        continue  # 네트워크 건너뛰기

    all_avg_shortest_paths.append(df["Average Shortest Path"].values)

# 최소 길이 확인
min_length = min(map(len, all_avg_shortest_paths))  # 가장 짧은 네트워크 길이에 맞춤
print("Minimum length across all networks:", min_length)

# Edge Attack Number 생성
edge_attack_number = np.arange(min_length)
avg_shortest_path_avg = np.mean(
    [paths[:min_length] for paths in all_avg_shortest_paths], axis=0
)


# 1. 평균 그래프 생성
max_avg = np.max(np.abs(avg_shortest_path_avg))
ylim_avg = 1.2 * max_avg  # y축 범위 설정 (최대값 기준)

plt.figure(figsize=(10, 6))
plt.plot(
    edge_attack_number,
    avg_shortest_path_avg,
    color="b",
    label="Average Shortest Path",
)
plt.xlabel("Edge Attack Number")
plt.ylabel("Average Shortest Path")
plt.title("Average Shortest Path vs Edge Attack Number")
plt.ylim(800, ylim_avg)
plt.xlim(0, 2426)  # x축 범위 설정
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(output_graph_dir, "average_shortest_path_graph.png"))
plt.close()

# 2. 첫 번째 미분 계산 및 그래프 생성
diff_avg_shortest_path = np.diff(avg_shortest_path_avg)
derivative_avg = diff_avg_shortest_path  # Remaining Edges가 아닌 Attack Number 기준

# y축 범위 설정: 미분값의 최대 절댓값 기준
max_derivative = np.max(np.abs(derivative_avg))
ylim_derivative = 1.2 * max_derivative  # y축 범위 설정 (최대값 기준)

# Linear Regression for First Derivative
slope, intercept = np.polyfit(edge_attack_number[:-1], derivative_avg, 1)
regression_line = slope * edge_attack_number[:-1] + intercept

plt.figure(figsize=(10, 6))
plt.plot(
    edge_attack_number[:-1],
    derivative_avg,
    color="r",
    label="Derivative of Average Shortest Path",
)
plt.plot(
    edge_attack_number[:-1],
    regression_line,
    "b--",
    label=f"Regression: y={slope:.2f}x+{intercept:.2f}",
)
plt.xlabel("Edge Attack Number")
plt.ylabel("Derivative of Average Shortest Path")
plt.title("Derivative of Average Shortest Path (Average)")
plt.ylim(0, ylim_derivative)
plt.xlim(0, 2426)  # x축 범위 설정
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(output_graph_dir, "average_derivative_graph.png"))
plt.close()

# 3. 두 번째 미분 계산 및 그래프 생성
second_derivative_avg = np.diff(derivative_avg)

# y축 범위 설정: 두 번째 미분값의 최대 절댓값 기준
max_second_derivative = np.max(np.abs(second_derivative_avg))
ylim_second_derivative = 1.2 * max_second_derivative  # y축 범위 설정 (최대값 기준)

# Linear Regression for Second Derivative
slope_2nd, intercept_2nd = np.polyfit(edge_attack_number[:-2], second_derivative_avg, 1)
regression_line_2nd = slope_2nd * edge_attack_number[:-2] + intercept_2nd

plt.figure(figsize=(10, 6))
plt.plot(
    edge_attack_number[:-2],
    second_derivative_avg,
    color="g",
    label="Second Derivative of Average Shortest Path",
)
plt.plot(
    edge_attack_number[:-2],
    regression_line_2nd,
    "b--",
    label=f"Regression: y={slope_2nd:.2f}x+{intercept_2nd:.2f}",
)
plt.xlabel("Edge Attack Number")
plt.ylabel("Second Derivative of Average Shortest Path")
plt.title("Second Derivative of Average Shortest Path (Average)")
plt.ylim(-ylim_second_derivative, ylim_second_derivative)
plt.xlim(0, 2426)  # x축 범위 설정
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(output_graph_dir, "average_second_derivative_graph.png"))
plt.close()

print("BA all graphs are saved.")
