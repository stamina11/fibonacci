
# Fibonacci API

This repository contains a simple Flask API that calculates the n<sup>th</sup> Fibonacci number.

## Repository Contents

- `fib.py`: The Python Flask application source code.
- `requirements.txt`: Python dependencies for the application.
- `Dockerfile`: Defines how to build the Docker image for the application.
- `docker-compose.yaml`: Configuration for running the application using Docker Compose.
- `kubernetes/`: Directory containing Kubernetes manifests.
  - `deployment.yaml`: Kubernetes Deployment definition.
  - `service.yaml`: Kubernetes Service definition.
  - `ingress.yaml`: Kubernetes Ingress definition for external access via Kong.
  - `argocd-application.yaml`: ArgoCD Application definition for GitOps deployment.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Git
- Python 3.9+
- pip (usually comes with Python)
- Docker (Docker Engine and Docker Compose)
- kubectl (for Kubernetes deployments)
- Access to a Kubernetes cluster (e.g., AKS, Minikube, Kind) with Kong Ingress Controller installed.
- ArgoCD CLI (if deploying with ArgoCD)

## How to Run and Test the API

The API exposes a single endpoint: `/fib?n=<number>`

Example: `http://localhost:5001/fib?n=10` will return `{"n": 10, "fibonacci": 55}`

### 1. Locally using Python Virtual Environment

Clone the repository:

```bash
git clone https://github.com/stamina11/fibonacci.git
cd fibonacci
```


Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate.bat  # On Windows (Command Prompt)
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python fib.py
```

The application will start on `http://0.0.0.0:5001`.

Test the API:

```bash
curl http://localhost:5001/fib?n=10
# Expected output: {"n": 10, "fibonacci": 55}
```

To stop the application, press `Ctrl+C`.
To deactivate the virtual environment, simply type `deactivate`.

### 2. In Docker

Build the Docker Image:

```bash
docker build -t stamina11/fibonacci-app:latest .
```

*(Replace `stamina11` with your Docker Hub username if needed)*

Run with `docker run`:

```bash
docker run -p 5001:5001 stamina11/fibonacci-app:latest
```

Run with `docker-compose`:

```bash
docker-compose up --build
```

Test the API:

```bash
curl http://localhost:5001/fib?n=10
# Expected output: {"n": 10, "fibonacci": 55}
```

To stop:

```bash
docker-compose down
```

Or for `docker run`:

```bash
Ctrl+C
docker rm <container_id>
```

### 3. In Kubernetes

Build and Push Docker Image:

```bash
docker build -t your-dockerhub-username/fibonacci-app:latest .
docker push your-dockerhub-username/fibonacci-app:latest
```

Update the image field in `kubernetes/deployment.yaml`.

Apply the manifests:

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/ingress.yaml
kubectl apply -f kubernetes/argocd-application.yaml
```

Update your DNS or `/etc/hosts` to point to `fibonacci.yourdomain.com`.

Test the API:

```bash
curl http://fibonacci.yourdomain.com/fib?n=10
# Expected output: {"n": 10, "fibonacci": 55}
```

To clean up:

```bash
kubectl delete -f kubernetes/ingress.yaml
kubectl delete -f kubernetes/service.yaml
kubectl delete -f kubernetes/deployment.yaml
kubectl delete -f kubernetes/argocd-application.yaml
```

## Production Deployment Considerations

### Containerization

- Use multi-stage builds for smaller image size.
- Run as non-root user.

### Continuous Integration/Deployment (CI/CD)

- CI: Automated tests, static analysis, image build/tag/push.
- CD: ArgoCD for GitOps-based deployments.

### Monitoring and Logging Strategies

- Use stdout/stderr logging.
- Centralized logging with ELK, Splunk, Loki, etc.
- Structured logs (JSON).

Monitoring:

- Prometheus + Grafana for metrics via Annotations
- Kubernetes liveness/readiness probes.
- Alerting on critical metrics.

### Scaling the Service

- HPA for autoscaling by CPU or custom metrics.
- VPA for resource optimization.
- Kong Ingress for load balancing.
