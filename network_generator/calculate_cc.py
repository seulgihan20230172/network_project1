import networkx as nx

# (1) 엣지리스트 파일을 불러온다
edge_list_file = "ER_network.csv"

# (2) 그래프 생성
G = nx.read_edgelist(
    edge_list_file, delimiter=",", create_using=nx.DiGraph(), data=[("weight", float)]
)

# (3) 클러스터링 계수 계산
# 전체 그래프의 평균 클러스터링 계수
average_clustering_coefficient = nx.average_clustering(G.to_undirected())

print(average_clustering_coefficient)
