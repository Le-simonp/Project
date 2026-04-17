Flask Monitor App
A simple Flask application with /health and /metrics endpoints that expose system resource information. Built as a lightweight monitoring utility.
Endpoints

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
