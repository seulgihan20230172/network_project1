import networkx as nx
import pandas as pd
import random
import matplotlib.pyplot as plt

# (1) test.csv 파일을 불러온다
df = pd.read_csv("test.csv")

# 가중치 리스트를 생성
weights = df["weight"].tolist()

# (2) 노드 수와 엣지 수를 변수로 지정한다
num_nodes = 50  # 노드 수
num_edges = 500  # 총 엣지 수

# 적절한 k 값을 계산 (총 간선 수를 맞추기 위해)
# WS 네트워크의 총 간선 수는 n * k // 2
k = num_edges // num_nodes

# (3) WS 네트워크 생성
ws_network = nx.watts_strogatz_graph(n=num_nodes, k=k, p=0.1)

# 방향성 추가
ws_network = ws_network.to_directed()

# 가중치를 랜덤으로 할당
used_weights = []
for u, v in ws_network.edges():
    if not weights:
        # 모든 가중치를 사용했다면 리셋
        weights = df["weight"].tolist()
        used_weights = []

    # 사용하지 않은 가중치 중에서 랜덤 선택
    available_weights = list(set(weights) - set(used_weights))

    # available_weights가 비어있으면 weights를 리셋
    if not available_weights:
        weights = df["weight"].tolist()
        used_weights = []
        available_weights = list(set(weights) - set(used_weights))

    weight = random.choice(available_weights)
    ws_network[u][v]["weight"] = weight
    used_weights.append(weight)

# (4) 엣지리스트를 csv파일로 저장한다.
# in-degree 혹은 out-degree가 0인 노드가 있는지 확인
has_zero_degree = any(
    ws_network.in_degree(n) == 0 or ws_network.out_degree(n) == 0
    for n in ws_network.nodes()
)

if has_zero_degree:
    print("경로가 없는 경로가 있음")
else:
    # 엣지 리스트를 저장
    nx.write_edgelist(ws_network, "WS_network.csv", data=["weight"])
