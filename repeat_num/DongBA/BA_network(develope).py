import networkx as nx
import pandas as pd
import random

# (1) test.csv 파일을 불러온다
df = pd.read_csv("test.csv")

# 가중치 리스트를 생성
weights = df["weight"].tolist()

# (2) 노드 수와 확률 p를 변수로 지정한다.
num_nodes = 50  # 예시로 50개의 노드
num_edges = 500  # 총 엣지 수

# ratio 계산
ratio = num_edges / num_nodes

# ratio의 소수점 부분을 p로 지정
p = ratio - int(ratio)

# (3) BA네트워크를 수동으로 생성한다.
G = nx.DiGraph()
G.add_nodes_from(range(num_nodes))

# 초기 완전 연결 그래프 생성
initial_nodes = 5
G.add_edges_from(
    (i, j) for i in range(initial_nodes) for j in range(initial_nodes) if i != j
)

for new_node in range(initial_nodes, num_nodes):
    targets = set()

    # 엣지 수를 확률적으로 결정
    num_edges_to_add = int(ratio) + 1 if random.random() < p else int(ratio)

    # 총 엣지 수를 절반으로 나누어 들어오는 엣지와 나가는 엣지를 설정
    num_incoming = num_edges_to_add // 2
    num_outgoing = num_edges_to_add - num_incoming

    # 들어오는 엣지 설정
    while len(targets) < num_incoming:
        potential_target = random.choice(list(G.nodes))
        if potential_target != new_node:
            targets.add((potential_target, new_node))

    # 나가는 엣지 설정
    while len(targets) < num_edges_to_add:
        potential_target = random.choice(list(G.nodes))
        if potential_target != new_node:
            targets.add((new_node, potential_target))

    G.add_edges_from(targets)

# 가중치를 랜덤으로 할당
used_weights = []
for u, v in G.edges():
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
    G[u][v]["weight"] = weight
    used_weights.append(weight)

# (4) 엣지리스트를 csv파일로 저장한다.
# in-degree 혹은 out-degree가 0인 노드가 있는지 확인
has_zero_degree = any(G.in_degree(n) == 0 or G.out_degree(n) == 0 for n in G.nodes())

if has_zero_degree:
    print("경로가 없음")
else:
    # 엣지 리스트를 저장
    nx.write_edgelist(G, "BA_network(develope).csv", data=["weight"])
