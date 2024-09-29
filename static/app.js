let dataset = [];
let clusters = [];
let centroids = [];
let initMethod = 'random';
let k = 3; 
let isManualSelected = false;


// Generate a new dataset (always 100 points)
function generateDataset() {
    k = document.getElementById('k-value').value;  // Get the number of clusters (k) from the input box

    fetch('/generate_dataset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ num_points: 100 })  // Always generate 100 points
    })
    .then(response => response.json())
    .then(data => {
        console.log('Dataset generated:', data.dataset);
        dataset = data.dataset;  // Store the dataset globally
        makePlot(dataset);  // Plot the dataset only, do not run KMeans
        manualCentroids();  // Ensure the listener is attached every time after plot re-rendering
    })
    .catch(error => console.error('Error generating dataset:', error));
}

// Enable manual centroid selection by clicking on the plot
function manualCentroids() {
    centroids = [];  // Clear any previous centroids
    isManualSelected = true;  // Enable manual centroid selection
    console.log('Manual centroid selection enabled.');

    let plotDiv = document.getElementById('plot');  // Get the plot div

    // // Remove previous listeners before adding a new one
    plotDiv.removeAllListeners('plotly_click');

    console.log("Attaching plotly_click listener");
    attachClickListener(plotDiv);

    // Plotly.purge(plotDiv);  // Clear the plot before re-rendering
    makePlot(dataset);  // Re-draw the plot with the dataset

    // // Attach a simple listener to log clicks
    // plotDiv.on('plotly_click', function(data) {
    //     console.log(`Clicked on plot at: (${data.points[0].x}, ${data.points[0].y})`);
    // });
}

function attachClickListener(plotDiv) {
    // const epsilon = 0.1;  // Tolerance for centroid selection
    plotDiv.on('plotly_click', function(data) {
        // Get the clicked coordinates
        let x = data.points[0].x;
        let y = data.points[0].y;

        // Add the selected point as a centroid if it's not already selected
        if (centroids.length < k) {
            centroids.push([x, y]);
            console.log(`Centroid selected at: (${x}, ${y}). Total centroids: ${centroids.length}`);

            // Update the plot with selected centroids
            makePlot(dataset, centroids);

            // Notify user once all centroids are selected
            if (centroids.length === k) {
                alert('You have selected all centroids. You can now run KMeans.');
            }
        } else {
            alert('Centroid selection limit reached.');
        }
        });
}

function runKMeans() {
    let k = parseInt(document.getElementById('k-value').value);  // Get the number of clusters (k)
    let initMethod = document.getElementById('init-method').value;

    console.log('Initialization method:', initMethod);
    console.log('Manual centroids (if applicable):', centroids);

    // Ensure all centroids are selected for manual method
    if (initMethod === 'manual' && centroids.length !== k) {
        alert(`Please select exactly ${k} centroids manually before running KMeans.`);
        return;  // Do not proceed if the centroids are not correctly selected
    }

    // First, call start_kmeans to initialize centroids and clusters
    fetch('/start_kmeans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            k: k,
            init_method: initMethod,
            manual_centroids: centroids  // Pass manual centroids if selected
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'error') {
            alert(data.message);
            console.log('Error:', data.message);
        } else {
            centroids = data.centroids;
            clusters = data.clusters;
            console.log(`KMeans started with centroids:`, centroids);
            makePlot(dataset, centroids, clusters);  // Update the plot after initialization

            // After centroids and clusters are initialized, run until convergence
            runUntilConvergence();  // Automatically step through until convergence
        }
    })
    .catch(error => console.error('Error during Run KMeans:', error));
}

function runUntilConvergence() {
    let k = parseInt(document.getElementById('k-value').value);  // Get the number of clusters (k)
    let initMethod = document.getElementById('init-method').value;

    fetch('/step_kmeans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            k: k,
            init_method: initMethod,
            manual_centroids: initMethod === 'manual' ? centroids : []  // Pass manual centroids if necessary
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'converged') {
            console.log('KMeans has converged!');
            alert('KMeans has converged!');
            makePlot(dataset, data.centroids, data.clusters);  // Final plot after convergence
        } else if (data.status === 'stepping') {
            centroids = data.centroids;
            clusters = data.clusters;
            console.log('Iteration:', data.iteration);
            makePlot(dataset, centroids, clusters);  // Update the plot after each step
            
            setTimeout(runUntilConvergence, 500);  // Continue iteration with delay
        }
    })
    .catch(error => console.error('Error during Run Until Convergence:', error));
}


// Step through KMeans one iteration at a time
function stepThroughKMeans() {
    fetch('/step_kmeans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            k: k,
            init_method: initMethod
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'converged') {
            console.log('KMeans has converged!');
            alert('KMeans has converged!');
        } else if (data.status === 'stepping') {
            centroids = data.centroids;
            clusters = data.clusters;
            console.log('Iteration:', data.iteration);
            makePlot(dataset, centroids, clusters);  // Update the plot with new clusters and centroids
        }
    })
    .catch(error => console.error('Error during step through KMeans:', error));
}

function makePlot(dataset = [], centroids = [], clusters = []) {
    let traces = [];
    const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']; // Distinct colors

    // Plot the clustered dataset points
    if (clusters.length > 0) {
        for (let i = 0; i < clusters.length; i++) {
            const clusterPoints = clusters[i];  // Get points for each cluster
            let clusterTrace = {
                x: clusterPoints.map(point => point[0]),  // X-coordinates of points
                y: clusterPoints.map(point => point[1]),  // Y-coordinates of points
                mode: 'markers',
                type: 'scatter',
                marker: { 
                    size: 10, 
                    color: colors[i % colors.length], 
                    opacity: 0.8, 
                    line: { width: 1, color: '#fff' }  // White outline for better visibility
                },
                name: `Cluster ${i + 1}`
            };
            traces.push(clusterTrace);
        }
    } else if (dataset.length > 0) {
        // Plot unclustered dataset points (if clusters are not available)
        let dataTrace = {
            x: dataset.map(point => point[0]),  // Extract x-coordinates
            y: dataset.map(point => point[1]),  // Extract y-coordinates
            mode: 'markers',
            type: 'scatter',
            marker: { 
                size: 10, 
                color: '#007BFF',  // Use a vibrant blue
                opacity: 1, 
                line: { width: 1, color: '#fff' }
            },
            name: 'Data Points'
        };
        traces.push(dataTrace);
    }

    // Plot the centroids if they exist
    if (centroids.length > 0) {
        let centroidTrace = {
            x: centroids.map(point => point[0]),  // X-coordinates of centroids
            y: centroids.map(point => point[1]),  // Y-coordinates of centroids
            mode: 'markers',
            type: 'scatter',
            marker: { 
                size: 14, 
                color: '#FF5733',  // Bright color for centroids
                symbol: 'cross', 
                opacity: 1, 
                line: { width: 2, color: '#fff' }
            },
            name: 'Centroids'
        };
        traces.push(centroidTrace);
    }

    let layout = {
        title: {
            text: `KMeans Clustering (k = ${k} Clusters)`,
            font: { size: 24 }
        },
        xaxis: { 
            title: 'X Axis', 
            titlefont: { size: 18 },
            tickfont: { size: 14 }
        },
        yaxis: { 
            title: 'Y Axis', 
            titlefont: { size: 18 },
            tickfont: { size: 14 }
        },
        plot_bgcolor: '#f9f9f9',  // Light background for contrast
        paper_bgcolor: '#f9f9f9',  // Match paper background
        showlegend: true,
        legend: {
            orientation: 'h',
            yanchor: 'bottom',
            y: 1.02,
            xanchor: 'center',
            x: 0.5
        }
    };

    // Update the plot without recreating it
    Plotly.react('plot', traces, layout);
}



function clearPlot() {
    Plotly.purge('plot');  // Clear the plot
    console.log('Plot cleared');
}

function resetAlgorithm() {
    console.log('Reset Button Used');

    fetch('/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'reset') {
            console.log('State has been reset');
            
            // Clear frontend state (centroids, clusters)
            centroids = [];
            clusters = [];

            // Log the dataset returned by the backend
            console.log('Dataset after reset:', data.dataset);
            
            // Check if dataset is properly defined before using it
            if (data.dataset && data.dataset.length > 0) {
                dataset = data.dataset;  // Assign the dataset from the backend to the global variable
                clearPlot(); // Clear existing plot
                makePlot(dataset);  // Re-plot the dataset (without centroids or clusters)
            } else {
                console.error('No dataset returned from the server after reset.');
            }
        }
    })
    .catch(error => console.error('Error during reset:', error));
}

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed');

    document.getElementById('generate-dataset').addEventListener('click', function() {
        console.log('Generate Dataset button used');
        generateDataset();
    });

    document.getElementById('run-kmeans').addEventListener('click', function() {
        console.log('Run KMeans button used');
        runKMeans();
    });

    document.getElementById('step-through').addEventListener('click', function() {
        console.log('Step Through KMeans button used');
        stepThroughKMeans();
    });

    document.getElementById('reset').addEventListener('click', function() {
        console.log('Reset button used');
        resetAlgorithm();
    });

    document.getElementById('init-method').addEventListener('change', function() {
        initMethod = document.getElementById('init-method').value;
        console.log('Initialization method changed to:', initMethod);

        if (initMethod === 'manual') {
            isManualSelected = true;
            manualCentroids();  // Enable manual centroid selection when manual is chosen
        } else {
            isManualSelected = false;
            console.log('Manual centroid selection disabled.');
        }
    });

    generateDataset(); // Always generate a new dataset on load
});

