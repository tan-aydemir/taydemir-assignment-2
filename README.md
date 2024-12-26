# KMeans Clustering Visualization Webpage

## Overview
The KMeans Clustering Visualization Webpage allows users to interactively explore the KMeans clustering algorithm and visualize its clustering process using different initialization strategies. It demonstrates the effect of various initialization methods on the clustering outcome.

## Features
This interactive web application provides the following functionality:

### Initialization Methods:
- **Random**: Centroids are randomly chosen from the data points.
- **Farthest First**: Initial centroids are selected to be as far apart as possible.
- **KMeans++**: Centroids are initialized to spread out, improving the algorithm's convergence.
- **Manual**: Users can manually select centroids by clicking on the data points.

### Visualization:
- **2D Plot**: Data points and centroids are displayed on a 2D plot.
- **Clustering Process**: Users can see the clustering process step-by-step, with clusters and centroids dynamically updated.
- **Manual Selection**: Users can click on the plot to manually select initial centroids.
- **Final Cluster Assignment**: Once the algorithm converges, the final cluster assignments are displayed.

### User Interface:
- **Drop-down Menu**: Users can choose an initialization method.
- **Generate Dataset**: A button to generate a new random dataset. The dataset remains unchanged when switching between initialization methods.
- **Step-by-Step Clustering**: A button to step through the clustering process, highlighting each step.
- **Go to Convergence**: A button to complete all steps of the algorithm at once.
- **Reset**: A button to reset the algorithm and select new initialization methods.

### Additional Requirements:
- **Makefile**: 
    - `make install`: Installs all required dependencies.
    - `make run`: Runs the web application locally on `http://localhost:3000`.

### GitHub Workflow Integration:
- Set up a GitHub Actions workflow to ensure the project builds and runs correctly by running `make install` and `make run`.

## Setup Instructions

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Install dependencies**:
    Use the `make install` command to install all necessary dependencies.
    ```bash
    make install
    ```

3. **Run the web application locally**:
    Use the `make run` command to start the web application on your local server at `http://localhost:3000`.
    ```bash
    make run
    ```

4. **Access the web application**:
    Open your browser and go to `http://localhost:3000` to interact with the application.

5. **Test the GitHub Actions Workflow**:
    Ensure the GitHub Actions workflow is set up correctly. The workflow should run `make install` and `make run` to verify your application runs as expected.

## Technologies Used
- **Frontend**: React.js, D3.js, or Plotly for rendering the interactive 2D plot.
- **Backend**: Flask (or a similar Python-based framework) to handle the server-side logic, if applicable.
- **Algorithm**: Implemented the KMeans clustering algorithm from scratch in Python (no external clustering libraries used).

## Evaluation Criteria
Your project will be evaluated based on the following:
- **Functionality**: All required features must be implemented and work as expected.
- **Code Quality**: Clean, readable, and maintainable code.
- **UI/UX**: The user interface should be intuitive and visually appealing.
- **Makefile**: The `make` commands should run correctly, setting up and running the project seamlessly.

## Submission
- **Demo Video**: Include a demo video showcasing the functionality of the application on your portfolio site. Alternatively, you can link to a YouTube video.
- **GitHub Repository**: Submit the link to the repository with your code and demo video.

## Conclusion
This project demonstrates an interactive approach to visualizing KMeans clustering and provides an in-depth look at the effects of different centroid initialization methods. The web application is designed to allow users to experiment with various settings, offering a clear and engaging learning experience.

