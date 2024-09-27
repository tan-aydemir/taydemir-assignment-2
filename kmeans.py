import numpy as np
import sklearn.datasets as datasets
import matplotlib.pyplot as plt
import sys

class KMeans:
    def __init__(self, data, k):
        self.data = data
        self.k = k
        self.assignment = [-1 for _ in range(len(data))]
        self.snaps = []

    # Init random method
    def initialize_random(self):
        np.random.seed(42)
        centroids = []
        m = np.shape(self.data)[0]

        for _ in range(self.k):
            r = np.random.randint(0, m-1)
            centroids.append(self.data[r])
        
        self.plot(self.data, np.array(centroids), "RANDOM")
        return np.array(centroids)

    # Init Kmeans++ Method
    def initialize_kmeanspp(self):
        # Randomly select the first centroid from the data
        centroids = [self.data[np.random.randint(self.data.shape[0])]]

        for _ in range(1, self.k):
            distances = np.array([
                min([self.eucledian_distance(point, c) for c in centroids])
                for point in self.data
            ])
            probabilities = distances / distances.sum()  # Normalize to get probabilities
            next_centroid_idx = np.random.choice(range(self.data.shape[0]), p=probabilities)
            centroids.append(self.data[next_centroid_idx])
        
        self.plot(self.data, np.array(centroids), "kmeans++")
        return np.array(centroids)


    # Init Farthest-First Method
    def initialize_farthest_first(self):
        initial_centroid_index = np.random.randint(self.data.shape[0])
        initial_centroid = self.data[initial_centroid_index]
        centroids = [initial_centroid]

        for i in range(1, self.k):
            distances = []
            for x in self.data:
                find_distance = self.eucledian_distance(x, centroids)
                distances.append(np.min(find_distance))

            max_index = np.argmax(distances)
            centroids.append(self.data[max_index])
        #self.plot(self.data, centroids)
        self.plot(self.data, np.array(centroids), "FARTHEST FIRST")
        return np.array(centroids)

    # Helper function to plot it:
        # Plotting the blobs
    def plot(self, data, centroids, name):    
        plt.scatter(data[:, 0], data[:, 1], c='blue', marker='o', edgecolor='k')
        plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=100, label='Centroids')

        plt.axhline(0, color='black', linewidth=2)  # Bold horizontal line
        plt.axvline(0, color='black', linewidth=2)  # Bold vertical line

        plt.title(f"Scatter plot of {name}")
        plt.xlabel("X1")
        plt.ylabel("X2")
        plt.grid(True)
        plt.show()

    # Helper function to find the Eucledian Distance between two coordinates. 
    def eucledian_distance(self, point, centroid):
        return np.sqrt(np.sum((point - centroid) ** 2))
    

    def lloyds(self):
        centers = self.initialize()
        self.make_clusters(centers)
        new_centers = self.compute_centers()
        self.snap(new_centers)
        while self.are_diff(centers, new_centers):
            self.unassign()
            centers = new_centers
            self.make_clusters(centers)
            new_centers = self.compute_centers()
            self.snap(new_centers)
        return

    
def test():
    n_samples = 300
    x_min, x_max = -10, 10
    y_min, y_max = -10, 10

    X = np.column_stack((
        np.random.uniform(x_min, x_max, n_samples),  # Random x coordinates
        np.random.uniform(y_min, y_max, n_samples)   # Random y coordinates
    ))

    k = 4
    kmeans = KMeans(X, k)
    
    #print(kmeans.initialize_kmeanspp())
    #print(kmeans.initialize_random())
    print(kmeans.initialize_farthest_first())

if __name__ == '__main__':
    test()
