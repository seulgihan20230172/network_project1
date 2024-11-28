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
ratio = num_edges / num_nodes

# ratio의 소수점 부분을 p로 지정
p = ratio - int(ratio)

# p의 확률로 rounded 값을 선택
# rounded = int(ratio) + 1 if random.random() < p else int(ratio)

# (3) BA네트워크를 생성한다.
G = nx.barabasi_albert_graph(
    num_nodes, int(ratio) + 1 if random.random() < p else int(ratio)
)
DG = G.to_directed()

# 가중치를 랜덤으로 할당
used_weights = []
for u, v in DG.edges():

    # 사용하지 않은 가중치 중에서 랜덤 선택
    available_weights = list(set(weights) - set(used_weights))

    # available_weights가 비어있으면 weights를 리셋
    if not available_weights:
        used_weights = []
        available_weights = list(set(weights) - set(used_weights))

    weight = random.choice(available_weights)
    DG[u][v]["weight"] = weight
    used_weights.append(weight)

# (4) 엣지리스트를 csv파일로 저장한다.
# in-degree 혹은 out-degree가 0인 노드가 있는지 확인
has_zero_degree = any(DG.in_degree(n) == 0 or DG.out_degree(n) == 0 for n in DG.nodes())

if has_zero_degree:
    print("경로가 없음")
else:
    # 엣지 리스트를 저장
    nx.write_edgelist(DG, "output.csv", data=["weight"])
