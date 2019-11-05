from commons import euclidean_distance
import random
import numpy as np


class DBSCAN:

    def __init__(self, data, eps, min_pts):
        self.data_length = len(data)
        self.data = np.array(data)
        self.eps = eps
        self.min_pts = min_pts
        self.num_of_cluster = 0
        self.cluster_points = []

        self.do_cluster()

    def process_neighbors(self):
        self.neighbors = [[] for _ in range(len(data))]
        for i in range(self.data_length):
            for j in range(self.data_length):
                if i != j and euclidean_distance(self.data[i], self.data[j]) <= self.eps:
                    self.neighbors[i].append(j)

    def do_cluster(self):
        np.random.shuffle(self.data)
        self.clusters = [None for _ in range(len(data))]

        self.process_neighbors()

        curr_cluster = 0
        for i in range(self.data_length):
            if self.clusters[i] is None and len(self.neighbors[i]) + 1 >= self.min_pts:
                self.apply_cluster(i, curr_cluster)
                curr_cluster += 1

        self.num_of_cluster = curr_cluster
        self.map_points_to_cluster()

    def apply_cluster(self, node, cluster):
        self.clusters[node] = cluster
        for next_node in self.neighbors[node]:
            if self.clusters[next_node] is None:
                self.apply_cluster(next_node, cluster)

    def map_points_to_cluster(self):
        self.cluster_points = [[] for _ in range(self.num_of_cluster)]
        for i in range(self.data_length):
            if self.clusters[i] is not None:
                self.cluster_points[self.clusters[i]].append(self.data[i])

    def get_all(self):
        return [(self.data[i], self.clusters[i]) for i in range(self.data_length)]

    def get_clusters(self, point):
        return self.clusters[np.where(self.data == point)[0]]

    def get_number_of_cluster(self):
        return self.num_of_cluster

    def get_points_from_cluster(self, cluster):
        return self.cluster_points[cluster]
