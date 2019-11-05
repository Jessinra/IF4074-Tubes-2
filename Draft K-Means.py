import numpy as np


class KMeans:

    def __init__(self, k=2, tol=0.001, max_iter=100):
        self.k = k
        self.tol = tol
        self.max_iter = max_iter
        self.data = None
        self.centroids = {}

        self._prev_centroids = {}
        self._optimized = False

    def fit_predict(self, data):
        self.fit(data)
        return self.predict(data)

    def fit(self, data):
        self.data = data
        self._init_centroids()

        for _ in range(self.max_iter):
            self._init_clusters()
            self._distribute_data_to_cluster()
            self._recalculate_centroids()
            self._evaluate_centroids()

            if self._optimized:
                break

    def predict(self, data):
        _distances = self._calculate_distances(data)
        return self._get_closest_cluster(_distances)

    def _init_centroids(self):
        self.centroids = {}
        self._prev_centroids = {}

        np.random.shuffle(self.data)
        self.centroids = {i: self.data[i] for i in range(self.k)}

    def _init_clusters(self):
        self.clusters = {i: [] for i in range(self.k)}

    def _distribute_data_to_cluster(self):
        """ Split dataset into k cluster """

        for data in self.data:
            _distances = self._calculate_distances(data)
            _cluster = self._get_closest_cluster(_distances)
            self.clusters[_cluster].append(data)

    def _recalculate_centroids(self):
        """ Recalculate new centroid using means of data inside the cluster """

        self._prev_centroids = dict(self.centroids)
        for cluster in self.clusters:
            self.centroids[cluster] = np.average(self.clusters[cluster], axis=0)

    def _evaluate_centroids(self):
        """ Check whether the centroid is optimized (final) """

        for c in self.centroids:
            _prev_cent = self._prev_centroids[c]
            _curr_cent = self.centroids[c]
            if np.sum((_curr_cent - _prev_cent) / _prev_cent * 100.0) <= self.tol:
                self._optimized = True
                return

    def _get_closest_cluster(self, distances):
        return distances.index(min(distances))

    def _calculate_distances(self, data):
        return [np.linalg.norm(data - self.centroids[centroid]) for centroid in self.centroids]

