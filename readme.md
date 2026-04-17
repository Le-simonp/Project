Flask Monitor App
A simple Flask application with /health and /metrics endpoints that expose system resource information. Built as a lightweight monitoring utility.
Endpoints
MethodEndpointDescriptionGET/App info and available endpointsGET/healthHealth check — returns healthy or degradedGET/metricsSystem metrics (CPU, memory, disk, network)
Example Responses

GET /health
json{
  "status": "healthy",
  "uptime": "0h 3m 12s",
  "issues": [],
  "timestamp": "2026-04-17T10:00:00Z"
}

GET /metrics
json{
  "system": {
    "hostname": "my-server",
    "os": "Linux",
    "architecture": "x86_64"
  },
  "cpu": {
    "usage_percent": 12.5,
    "logical_cores": 4,
    "physical_cores": 2
  },
  "memory": {
    "total_mb": 8192.0,
    "used_mb": 3200.0,
    "usage_percent": 39.1
  },
  "disk": {
    "total_gb": 50.0,
    "used_gb": 18.3,
    "usage_percent": 36.6
  },
  "network": {
    "bytes_sent_mb": 120.5,
    "bytes_recv_mb": 340.2
  },
  "app_uptime": "0h 3m 12s",
  "timestamp": "2026-04-17T10:00:00Z"
}

# Running Locally
Without Docker
bash# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
App will be available at http://localhost:5000
With Docker
bash# Build image
docker build -t flask-monitor-app .

# Run container
docker run -p 5000:5000 flask-monitor-app
Environment Variables
VariableDefaultDescriptionPORT5000Port to run the app onFLASK_DEBUGfalseEnable debug mode
Tech Stack

Python 3.12
Flask — web framework
psutil — system metrics library
