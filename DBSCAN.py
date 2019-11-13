from commons import euclidean_distance
import random, math
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
        self.neighbors = [[] for _ in range(len(self.data))]
        for i in range(self.data_length):
            for j in range(self.data_length):
                if i != j and euclidean_distance(self.data[i], self.data[j]) <= self.eps:
                    self.neighbors[i].append(j)

    def do_cluster(self):
        indices = [i for i in range(len(self.data))]
        random.shuffle(indices)
        self.clusters = [None for _ in range(len(self.data))]

        self.process_neighbors()

        curr_cluster = 0
        for i in indices:
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
        return self.clusters

    def get_clusters(self, point):
        return self.clusters[np.where(self.data == point)[0]]

    def get_number_of_cluster(self):
        return self.num_of_cluster

    def get_points_from_cluster(self, cluster):
        return self.cluster_points[cluster]

    def predict(self, point):
        # Option 1 find the nearest to one of core point in cluster
        result_cluster = None
        min_dist = self.eps + 1
        point = np.array(point)
        for i in range(len(self.data)):
            if len(self.neighbors[i]) + 1 >= self.min_pts:
                distance = euclidean_distance(point, self.data[i])
                if distance <= self.eps and distance <= min_dist :
                    result_cluster = self.clusters[i]
                    min_dist = distance

        return result_cluster

        # Option 2 find the nearest centroid of cluster
        min_dist = math.inf
        for i in range(self.num_of_cluster):
            sum = np.array([0 for _ in range(len(self.data[0]))])
            size = len(self.cluster_points)
            for p in self.cluster_points:
                sum += p / size
            distance = euclidean_distance(sum, point)
            if min_dist < distance:
                min_dist = distance
                result_cluster = i

        return result_cluster
