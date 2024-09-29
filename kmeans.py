import numpy as np

class KMeans:
    def __init__(self, k=3, max_iterations=100, initialization_method='random'):
        self.k = k
        # Set max iterations to 100
        self.max_iterations = max_iterations
        self.initalization_method = initialization_method
        self.centroids = None
        self.labels = None
        self.num_iterations = 0

    def initialize(self, data):
        if self.initalization_method == 'farthest_first':
            self.centroids = self.farthest_first(data)
        elif self.initalization_method == 'kmeans++':
            self.centroids = self.kmeanspp(data)
        elif self.initalization_method == 'random':
            self.centroids = data[np.random.choice(data.shape[0], self.k, replace=False)]

    def step(self, data):
        if self.centroids is None:
            self.initialize(data)
        else:
            prev_centroids = self.centroids.copy()
            self.labels = self.assign_labels(data)
            self.update_centroids(data)
            self.num_iterations += 1
            if np.all(prev_centroids == self.centroids):
                return False
        return True
    
    def fit(self, data):
        self.initialize(data)
        for a in range(self.max_iterations):
            prev_centroids = self.centroids.copy()
            self.labels = self.assign_labels(data)
            self.update_centroids(data)
            self.num_iterations += 1
            if np.all(prev_centroids == self.centroids):
                break

    def farthest_first(self, X):
        centroids = [X[np.random.choice(X.shape[0])]]
        for _ in range(1, self.k):
            dists = np.array([min([np.linalg.norm(x - c) for c in centroids]) for x in X])
            centroids.append(X[np.argmax(dists)])
        return np.array(centroids)

    def kmeanspp(self, X):
        centroids = [X[np.random.choice(X.shape[0])]]
        for _ in range(1, self.k):
            dists = np.array([min([np.linalg.norm(x - c) for c in centroids]) for x in X])
            probs = dists**2 / np.sum(dists**2)
            centroids.append(X[np.random.choice(X.shape[0], p=probs)])
        return np.array(centroids)

    def assign_labels(self, X):
        return np.array([np.argmin([np.linalg.norm(x - c) for c in self.centroids]) for x in X])

    def update_centroids(self, X):
        for i in range(self.k):
            if np.sum(self.labels == i) > 0:
                self.centroids[i] = np.mean(X[self.labels == i], axis=0)

    def predict(self, X):
        return self._assign_labels(X)