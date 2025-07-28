Fibonacci API
This repository contains a simple Flask API that calculates the n 
th
  Fibonacci number.

Repository Contents
fib.py: The Python Flask application source code.

requirements.txt: Python dependencies for the application.

Dockerfile: Defines how to build the Docker image for the application.

docker-compose.yaml: Configuration for running the application using Docker Compose.

kubernetes/: Directory containing Kubernetes manifests.

kubernetes/deployment.yaml: Kubernetes Deployment definition.

kubernetes/service.yaml: Kubernetes Service definition.

kubernetes/ingress.yaml: Kubernetes Ingress definition for external access via Kong.

kubernetes/argocd-application.yaml: ArgoCD Application definition for GitOps deployment.

Prerequisites
Before you begin, ensure you have the following installed on your system:

Git

Python 3.9+

pip (usually comes with Python)

Docker (Docker Engine and Docker Compose)

kubectl (for Kubernetes deployments)

Access to a Kubernetes cluster (e.g., AKS, Minikube, Kind) with Kong Ingress Controller installed.

ArgoCD CLI (if deploying with ArgoCD)

How to Run and Test the API
The API exposes a single endpoint: /fib?n=<number>.

Example: http://localhost:5001/fib?n=10 will return {"n": 10, "fibonacci": 55}.

1. Locally using Python Virtual Environment
This method allows you to run the application directly on your machine using a Python virtual environment, which isolates its dependencies.

Clone the repository:

git clone https://github.com/stamina11/fibonacci.git
cd fibonacci

(Note: If you are using a specific SSH alias for your GitHub account, adjust the clone URL accordingly, e.g., git clone git@github.com-personal:stamina11/fibonacci.git)

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate.bat  # On Windows (Command Prompt)
# venv\Scripts\Activate.ps1  # On Windows (PowerShell)

Install dependencies:

pip install -r requirements.txt

Run the application:

python fib.py

The application will start on http://0.0.0.0:5001.

Test the API:
Open your web browser or use curl:

curl http://localhost:5001/fib?n=10
# Expected output: {"n": 10, "fibonacci": 55}

To stop the application, press Ctrl+C in the terminal where it's running.
To deactivate the virtual environment, simply type deactivate.

2. In Docker
This method packages your application into a Docker image, allowing it to run consistently across different environments.

Build the Docker Image:
Navigate to the root of your fibonacci project directory (where Dockerfile is located).

docker build -t stamina11/fibonacci-app:latest .

(Replace stamina11 with your Docker Hub username if you plan to push it to your own registry).

Run with docker run:
This command runs the Docker image directly.

docker run -p 5001:5001 stamina11/fibonacci-app:latest

-p 5001:5001: Maps port 5001 on your host machine to port 5001 inside the container.

Run with docker-compose:
For easier management of multi-container applications (even if only one here), use Docker Compose. Ensure docker-compose.yaml is in your project root.

docker-compose up --build

--build: Ensures the Docker image is built (or rebuilt) before starting the container.

Test the API:
Open your web browser or use curl:

curl http://localhost:5001/fib?n=10
# Expected output: {"n": 10, "fibonacci": 55}

To stop and remove the Docker containers (if using docker-compose):

docker-compose down

To stop the docker run container, press Ctrl+C in its terminal, then docker rm <container_id> if it doesn't stop automatically.

3. In Kubernetes
Deploying to Kubernetes involves creating declarative YAML files that describe your desired application state (Deployment) and how to access it (Service). For external access, an Ingress resource is used, which in this case is managed by the Kong Ingress Controller.

Build and Push Docker Image:
First, ensure your Docker image is built and pushed to a container registry that your Kubernetes cluster can access (e.g., Docker Hub, Azure Container Registry).

docker build -t your-dockerhub-username/fibonacci-app:latest .
docker push your-dockerhub-username/fibonacci-app:latest

Important: Update the image field in kubernetes/deployment.yaml to point to your pushed image (e.g., image: your-dockerhub-username/fibonacci-app:latest).

Kubernetes Manifests:
The kubernetes/ directory contains deployment.yaml, service.yaml, and ingress.yaml. These files define:

Deployment: Manages the lifecycle of your application's pods (containers).

Service: Provides a stable network endpoint to access your application within the cluster.

Ingress: Exposes your service externally via a hostname, managed by the Kong Ingress Controller.

Deploy to Kubernetes:
Apply the Kubernetes manifests to your cluster. Ensure Kong Ingress Controller is already installed and running in your cluster.

kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml

Note: You must update fibonacci.yourdomain.com in kubernetes/ingress.yaml to a domain you control and configure its DNS to point to your Kong Ingress Controller's external IP.

Test the API:

Get Kong Ingress Controller External IP:

kubectl get svc -n kong # Or wherever your Kong service is

Look for the EXTERNAL-IP of the Kong proxy service.

Update your local /etc/hosts (for testing):
Add an entry like this, replacing <KONG_EXTERNAL_IP> with the IP you found and fibonacci.yourdomain.com with the hostname you set in ingress.yaml:

<KONG_EXTERNAL_IP> fibonacci.yourdomain.com

Access the API:

curl http://fibonacci.yourdomain.com/fib?n=10
# Expected output: {"n": 10, "fibonacci": 55}

To clean up the deployment:

kubectl delete -f kubernetes/ingress.yaml
kubectl delete -f kubernetes/service.yaml
kubectl delete -f kubernetes/deployment.yaml

Production Deployment Considerations
Containerization
The application is containerized using Docker, which provides a consistent and isolated environment for running the service. For production, the Dockerfile should be optimized for smaller image size (e.g., using multi-stage builds) and security (e.g., running as a non-root user). A production-ready WSGI server like Gunicorn should be used instead of Flask's built-in development server.

Continuous Integration/Continuous Deployment (CI/CD)
For automated deployments, a CI/CD pipeline is essential.

CI (Continuous Integration):

Automated tests (unit, integration) triggered on every code commit.

Static code analysis.

Docker image build and tagging (e.g., with Git commit SHA or version number).

Pushing the Docker image to a secure container registry.

CD (Continuous Deployment):

ArgoCD (GitOps): This application is designed to be deployed using ArgoCD. The kubernetes/argocd-application.yaml defines how ArgoCD should monitor a Git repository (this one, or a dedicated GitOps repository) for Kubernetes manifest changes and automatically synchronize them to the cluster. This ensures that the desired state in Git is always reflected in the cluster.

Deployment Strategy: Implement strategies like rolling updates (default Kubernetes behavior) for zero-downtime deployments. Consider blue/green or canary deployments for more controlled rollouts in critical environments.

Monitoring and Logging Strategies
Logging:

Configure the Flask application to log to stdout and stderr.

Use a centralized logging solution (e.g., ELK Stack - Elasticsearch, Logstash, Kibana; or Splunk, Datadog, Prometheus Loki) to collect logs from all pods.

Ensure logs are structured (e.g., JSON format) for easier parsing and analysis.

Monitoring:

Metrics: Use Prometheus and Grafana for collecting and visualizing application and infrastructure metrics (CPU, memory, network I/O, request latency, error rates).

Health Checks: Implement Kubernetes liveness and readiness probes in the Deployment YAML to ensure pods are healthy and ready to receive traffic.

Alerting: Set up alerts based on critical metrics (e.g., high error rates, low available replicas) to notify operations teams.

Scaling the Service
Horizontal Pod Autoscaler (HPA): Configure Kubernetes HPA to automatically scale the number of pods based on CPU utilization or custom metrics (e.g., requests per second). This ensures the service can handle varying loads.

Vertical Pod Autoscaler (VPA): Consider VPA for recommending optimal CPU and memory requests/limits for pods, or even automatically adjusting them, to ensure efficient resource utilization.

Load Balancing: Kubernetes Ingress (via Kong) provides advanced load balancing and routing capabilities.

Database/External Dependencies: Ensure any external dependencies (like databases) are also scalable and highly available to avoid becoming bottlenecks.

