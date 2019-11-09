import math
from commons import euclidean_distance


class Agglomerative:
    def __init__(self, data, k, linkage_type):
        self.k = k
        self.data = data
        self.data_length = len(data)
        self.groups = []
        set_linkage_function(linkage_type)

        fit()

    def set_linkage_function(self, linkage_type):
        #TODO: FILL the three dots
        if linkage_type == 'single':
            self.linkage_function =  self.single_linkage
        elif linkage_type == 'complete':
            self.linkage_function =  self.complete_linkage
        elif linkage_type == 'average':
            self.linkage_function =  self.average_linkage
        elif linkage_type == 'average_group':
            self.linkage_function =  self.average_group_linkage

    def init_group(self):
        self.num_of_group = self.data_length
        self.group = [[i] for i in range(self.data_length)]

    def init_dist_array(self):
        self.dist_array = []
        i = 0
        while i < self.data_length:
            j = i + 1
            while j < self.data_length:
                self.dist_array.append((self.linkage_function(self.group[i], self.group[j]), i, j))
        self.dist_array = sorted(self.dist_array, key = lambda x : x[0])

    def fit(self):
        self.init_group()
        self.init_dist_array()

        while self.num_of_group > k:
            curr = self.dist_array.pop(0)
            self.join_group(curr[1], curr[2])
            self.num_of_group -= 1

        self.set_cluster_groups()

    def join_group(self, group1, group2):
        self.group[group1] = self.group[group1] + self.group[group2]
        self.group[group2] = []
        self.dist_array = [item for item in self.dist_array if item[1] != group2 and item[2] != group2]
        for i in range(len(self.dist_array)):
            if self.dist_array[i][1] == group1 or self.dist_array[i][2] == group1:
                self.dist_array = self.linkage_function(self.group[self.dist_array[i][1]], self.dist_array[i][2])
        self.dist_array = sorted(self.dist_array, key = lambda x : x[0])

    def set_cluster_groups(self):
        self.clusters = []
        for party in self.group:
            points = []
            for member_id in party:
                points.append(self.data[member_id])
            self.clusters.append(points)

    def get_all(self):
        return self.clusters

    def single_linkage(self, points_a, points_b):
        min_dist = math.inf
        for idx_a in points_a:
            for idx_b in points_b:
                min_dist = min(min_dist, euclidean_distance(self.data[idx_a], self.data[idx_b]))
        return min_dist

    def complete_linkage(self, points_a, points_b):
        max_dist = 0
        for idx_a in points_a:
            for idx_b in points_b:
                max_dist = max(max_dist, euclidean_distance(self.data[idx_a], self.data[idx_b]))
        return max_dist

    def average_linkage(self, points_a, points_b):
        dist = 0
        num_of_pair = len(points_a) * len(points_b)
        for idx_a in points_a:
            for idx_b in points_b:
                dist += euclidean_distance(self.data[idx_a], self.data[idx_b]) / num_of_pair
        return dist

    def average_group_linkage(self, points_a, points_b):
        dimension = len(self.data[0])
        avg_a = [0 for _ in range(dimension)]
        avg_b = [0 for _ in range(dimension)]
        for idx_a in points_a:
            for i in range(dimension):
                avg_a[i] += self.data[idx_a][i] / len(points_a)
        for idx_b in points_b:
            for i in range(dimension):
                avg_b[i] += self.data[idx_b][i] / len(points_b)
        return euclidean_distance(avg_a, avg_b)