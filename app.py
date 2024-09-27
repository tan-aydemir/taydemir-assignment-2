from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import numpy as np
from PIL import Image
from io import BytesIO
from sklearn.cluster import KMeans
from kmeans import KMeans

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-kmeans', methods=['POST'])

def run_kmeans():
    method = request.json['method']
    data = request.json['data']
    
    # Convert data to numpy array
    data = np.array(data)

    # clusters
    k = 4
    
    kmeans = KMeans(data, k)  # Example with 4 clusters
    # Random algorithm
    if method == 'random':
        kmeans.initialize_random()
    
    # Farthest-first algorithm
    elif method == 'farthest':
        kmeans.initialize_farthest_first()

    # Kmeans++ algorithm
    elif method == 'kmeans++':
        kmeans.initialize_kmeanspp()

    kmeans.lloyds()

    return jsonify({"snapshots": kmeans.get_snapshots()})



if __name__ == '__main__':
    app.run(debug = True)