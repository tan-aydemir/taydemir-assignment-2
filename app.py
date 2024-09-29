from flask import Flask, jsonify, request, render_template
import numpy as np
import random

app = Flask(__name__)

# Global variables for tracking KMeans state
data_coordinates = []
centroids = []
clusters = []
iteration = 0
max_iterations = 100

@app.route('/')
def index():
    return render_template('index.html')

def init_random(data, k):
    if len(data) == 0:
        raise ValueError("Dataset is empty")
    return random.sample(data, k)


def init_kmeans_plus_plus(data, k):
    if len(data) == 0:
        raise ValueError("Dataset is empty")
    centroids = [random.choice(data)]
    for _ in range(1, k):
        distances = [min([np.linalg.norm(np.array(p) - np.array(c)) for c in centroids]) for p in data]
        new_centroid = random.choices(data, weights=distances, k=1)[0]
        centroids.append(new_centroid)    
    print(f"Final centroids after KMeans++ initialization: {centroids}")
    return centroids


def init_farthest_first(data, k):
    """ Farthest first algorithm """
    centroids = [random.choice(data)]  # Start with a random point
    for _ in range(1, k):
        farthest_point = max(data, key=lambda p: min([np.linalg.norm(np.array(p) - np.array(c)) for c in centroids]))
        centroids.append(farthest_point)
    return centroids


def assign_clusters(data, centroids):
    """ Assign each point to the nearest centroid """
    if len(centroids) == 0:
        raise ValueError("No centroids")
    
    clusters = [[] for _ in centroids]
    for point in data:
        distances = [np.linalg.norm(np.array(point) - np.array(centroid)) for centroid in centroids]
        cluster_index = np.argmin(distances)
        clusters[cluster_index].append(point)
    return clusters


def compute_centroid_means(clusters):
    """ Compute centroids as the mean of points within the cluster """
    new_centroids = [np.mean(cluster, axis=0).tolist() for cluster in clusters if len(cluster) > 0]
    return new_centroids


@app.route('/generate_dataset', methods=['POST'])
def generate_dataset():
    """ Generate a new random dataset and store it globally """
    global data_coordinates
    global iteration
    num_points = int(request.json['num_points'])
    data_coordinates = np.random.rand(num_points, 2).tolist() 
    iteration = 0 
    return jsonify({'dataset': data_coordinates})  


@app.route('/start_kmeans', methods=['POST'])
def start_kmeans():
    global centroids, clusters, iteration
    k = int(request.json['k'])
    initialization_method = request.json['init_method']
    
    # Ensure dataset exists
    if len(data_coordinates) == 0:
        return jsonify({'status': 'error', 'message': 'No dataset available. Please generate the dataset first.'}), 400
    
    # Handle manual centroids
    if initialization_method == 'manual':
        centroids = request.json.get('manual_centroids', [])
        if len(centroids) != k:
            return jsonify({'status': 'error', 'message': 'Incorrect number of manual centroids.'}), 400
    else:
        # Other initialization methods
        if initialization_method == 'random':
            centroids = init_random(data_coordinates, k)
        elif initialization_method == 'kmeans++':
            centroids = init_kmeans_plus_plus(data_coordinates, k)
        elif initialization_method == 'farthest_first':
            centroids = init_farthest_first(data_coordinates, k)

    # Assign initial clusters
    clusters = assign_clusters(data_coordinates, centroids)
    iteration = 1  # Reset iteration
    
    return jsonify({'centroids': centroids, 'clusters': clusters})

@app.route('/step_kmeans', methods=['POST'])
def step_kmeans():
    global centroids, clusters, iteration, data_coordinates
    k = int(request.json['k'])
    init_method = request.json['init_method']
    
    print(f"Step Through KMeans called with k={k}, init_method={init_method}")

    # Ensure centroids are available
    if len(centroids) == 0:
        print(f"No centroids found. Initializing centroids using {init_method}.")

        if init_method == 'manual':
            centroids = request.json.get('manual_centroids', [])
            if len(centroids) != k:
                return jsonify({'status': 'error', 'message': 'Incorrect number of manual centroids.'}), 400
        else:
            # Initialization methods for other types
            centroids = init_random(data_coordinates, k) if init_method == 'random' else init_kmeans_plus_plus(data_coordinates, k)
        
        clusters = assign_clusters(data_coordinates, centroids)
        iteration = 1  # Reset iteration
        return jsonify({'centroids': centroids, 'clusters': clusters, 'status': 'stepping', 'iteration': iteration})

    # Step through the algorithm by reassigning clusters and recomputing centroids
    clusters = assign_clusters(data_coordinates, centroids)
    new_centroids = compute_centroid_means(clusters)

    # Check for convergence
    if new_centroids == centroids or iteration >= max_iterations:
        print("Convergence reached.")
        return jsonify({'status': 'converged', 'centroids': centroids, 'clusters': clusters})

    # Update centroids and increment iteration count
    centroids = new_centroids
    iteration += 1

    return jsonify({'status': 'stepping', 'centroids': centroids, 'clusters': clusters, 'iteration': iteration})



@app.route('/reset', methods=['POST'])
def reset():
    """ Reset the algorithm but keep the dataset """
    global centroids, clusters, iteration, data_coordinates
    print("What does this print?")
    # Ensure the dataset still exists
    if len(data_coordinates) == 0:
        return jsonify({'status': 'error', 'message': 'No dataset found to reset.'}), 400
    
    # Clear centroids and clusters, but keep the dataset
    centroids = []
    clusters = []
    iteration = 0  # Reset iteration count
        
    # Return the existing dataset in the response
    return jsonify({'status': 'reset', 'dataset': data_coordinates})



if __name__ == '__main__':
    app.run(port=3000, debug=True)
