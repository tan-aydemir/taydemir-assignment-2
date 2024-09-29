from flask import Flask, jsonify, request, render_template
import numpy as np
import random

app = Flask(__name__)

dataset = []
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


def initialize_farthest_first(data, k):
    centroids = [random.choice(data)]  # Start with a random point
    for _ in range(1, k):
        farthest_point = max(data, key=lambda p: min([np.linalg.norm(np.array(p) - np.array(c)) for c in centroids]))
        centroids.append(farthest_point)
    return centroids


def initialize_kmeans_plus_plus(data, k):
    if len(data) == 0:
        raise ValueError("Empty dataset.")
    
    # Start with one random centroid
    centroids = [random.choice(data)]
    print(f"First centroid (KMeans++): {centroids}")
    
    for _ in range(1, k):
        # Calculate distances for every point to the nearest centroid
        distances = [min([np.linalg.norm(np.array(p) - np.array(c)) for c in centroids]) for p in data]
                
        # Select a new centroid based on the weighted probability distribution
        new_centroid = random.choices(data, weights=distances, k=1)[0]
        centroids.append(new_centroid)
    
    return centroids


def assign_clusters(data, centroids):
    if len(centroids) == 0:
        raise ValueError("No centroids provided.")
    
    clusters = [[] for _ in centroids]
    for point in data:
        distances = [np.linalg.norm(np.array(point) - np.array(centroid)) for centroid in centroids]
        cluster_index = np.argmin(distances)
        clusters[cluster_index].append(point)
    return clusters


def recompute_centroids(clusters):
    new_centroids = [np.mean(cluster, axis=0).tolist() for cluster in clusters if len(cluster) > 0]
    return new_centroids


@app.route('/generate_dataset', methods=['POST'])
def generate_dataset():
    global dataset, iteration
    num_points = int(request.json['num_points'])
    dataset = np.random.rand(num_points, 2).tolist()  # Generate random 2D points
    iteration = 0  # Reset iteration
    print(f"New dataset generated with {num_points} points.")
    
    return jsonify({'dataset': dataset})  # Return the dataset to the frontend


@app.route('/step_kmeans', methods=['POST'])
def step_kmeans():
    global centroids, clusters, iteration, dataset
    k = int(request.json['k'])
    init_method = request.json['init_method']
    
    # Ensure centroids are available
    if len(centroids) == 0:

        if init_method == 'manual':
            # Get the manual centroids from the request
            centroids = request.json.get('manual_centroids', [])
            # If the number of centroids is incorrect, return an error
            if len(centroids) != k:
                return jsonify({'status': 'error', 'message': f'Please select exactly {k} centroids manually.'}), 400
        else:
            # Handle other initialization methods
            if init_method == 'random':
                centroids = init_random(dataset, k)
            elif init_method == 'kmeans++':
                centroids = initialize_kmeans_plus_plus(dataset, k)
            elif init_method == 'farthest_first':
                centroids = initialize_farthest_first(dataset, k)
        
        clusters = assign_clusters(dataset, centroids)
        iteration = 1  # Reset iteration count
        return jsonify({'centroids': centroids, 'clusters': clusters, 'status': 'stepping', 'iteration': iteration})

    clusters = assign_clusters(dataset, centroids)
    new_centroids = recompute_centroids(clusters)

    # Check for convergence
    if new_centroids == centroids or iteration >= max_iterations:
        return jsonify({'status': 'converged', 'centroids': centroids, 'clusters': clusters})

    # Update centroids and increment iteration count
    centroids = new_centroids
    iteration += 1

    print(f"Step-through complete. Iteration {iteration}.")
    return jsonify({'status': 'stepping', 'centroids': centroids, 'clusters': clusters, 'iteration': iteration})

@app.route('/reset', methods=['POST'])
def reset():
    global centroids, clusters, iteration, dataset

    # Check if the dataset still exists
    if len(dataset) == 0:
        return jsonify({'status': 'error', 'message': 'No dataset found to reset.'}), 400
    
    # Clear centroids and clusters, but keep the dataset
    centroids = []
    clusters = []
    iteration = 0  # Reset iteration count
    
    
    # Return the existing dataset in the response
    return jsonify({'status': 'reset', 'dataset': dataset})


@app.route('/start_kmeans', methods=['POST'])
def start_kmeans():
    global centroids, clusters, iteration
    k = int(request.json['k'])
    init_method = request.json['init_method']
    
    # Ensure dataset exists
    if len(dataset) == 0:
        return jsonify({'status': 'error', 'message': 'No dataset available. Please generate the dataset first.'}), 400
    
    # Handle manual centroids
    if init_method == 'manual':
        centroids = request.json.get('manual_centroids', [])
        if len(centroids) != k:
            return jsonify({'status': 'error', 'message': 'Incorrect number of manual centroids.'}), 400
    else:
        # Other initialization methods
        if init_method == 'random':
            centroids = init_random(dataset, k)
        elif init_method == 'kmeans++':
            centroids = initialize_kmeans_plus_plus(dataset, k)
        elif init_method == 'farthest_first':
            centroids = initialize_farthest_first(dataset, k)

    # Assign initial clusters
    clusters = assign_clusters(dataset, centroids)
    iteration = 1  # Reset iteration
    
    return jsonify({'centroids': centroids, 'clusters': clusters})

if __name__ == '__main__':
    app.run(port=3000, debug=True)
