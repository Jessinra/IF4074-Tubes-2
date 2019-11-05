LINKAGE_TYPE = {
    'single': 1,
    'complete': 2,
    'avarage': 3,
    'average_group': 4,
}

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
            self.linkage_function =  ...
        elif linkage_type == 'complete':
            self.linkage_function =  ...
        elif linkage_type == 'average':
            self.linkage_function =  ...
        elif linkage_type == 'average_group':
            self.linkage_function =  ...

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
        sorted(self.dist_array, key = lambda x : x[0])

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
        sorted(self.dist_array, key = lambda x : x[0])

    def set_cluster_groups(self):
        self.clusters = []
        for party in self.group:
            points = []
            for member_id in party:
                points.append(self.data[member_id])
            self.clusters.append(points)

    def get_all(self):
        return self.clusters