import networkx as nx
import pandas as pd
import random

# (1) test.csv 파일을 불러온다
weights_df = pd.read_csv("test.csv")

# 가중치 리스트 생성
weights = list(weights_df["weight"])

# (2) 노드 수와 확률 p를 변수로 지정한다.
num_nodes = 50  # 예시로 10개의 노드
num_egdes = 500
p = (num_egdes) / (num_nodes * (num_nodes - 1))  # 엣지 생성 확률


# (3) ER네트워크를 생성한다.
def create_er_network(num_nodes, p, weights):
    G = nx.DiGraph()  # 방향성 있는 그래프 생성
    G.add_nodes_from(range(num_nodes))

    used_weights = []

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < p:
                if not weights:
                    # 모든 가중치를 사용했다면 리셋
                    weights = used_weights
                    used_weights = []

                # 가중치 랜덤 선택 및 사용
                weight = random.choice(weights)
                weights.remove(weight)
                used_weights.append(weight)

                G.add_edge(i, j, weight=weight)

    return G


# 네트워크 생성
G = create_er_network(num_nodes, p, weights)


# (4) 엣지리스트를 csv파일로 저장한다.
def save_network_to_csv(G, filename):
    # in-degree 혹은 out-degree가 0인 노드가 있는지 확인
    for node in G.nodes():
        if G.in_degree(node) == 0 or G.out_degree(node) == 0:
            print("경로가 없는 경로가 있음")
            return
    # Save the graph as an edge list with weights
    nx.write_edgelist(G, filename, delimiter=",", data=["weight"])


# 네트워크 저장
save_network_to_csv(G, "ER_network.csv")
