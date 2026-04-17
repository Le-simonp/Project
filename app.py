from flask import Flask,jsonify
import psutil
import platform
import datetime
import os

app = Flask(__Stats__)

START_TIME = datetime.datetime.utcnow()


def get_uptime():
    delta = datetime.datetime.utcnow() - START_TIME
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"


@app.route("/")
def index():
    return jsonify({
        "app": "Monitor App",
        "version": "1.0.0",
        "description": "A simple Flask app with health and metrics endpoints",
        "endpoints": {
            "GET /": "App info (this response)",
            "GET /health": "Health check status",
            "GET /metrics": "System resource metrics"
        },
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


@app.route("/health")
def health():
    cpu = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory()

    status = "healthy"
    issues = []

    if cpu > 90:
        issues.append("High CPU usage")
        status = "degraded"
    if memory.percent > 90:
        issues.append("High memory usage")
        status = "degraded"

    return jsonify({
        "status": status,
        "uptime": get_uptime(),
        "issues": issues,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }), 200 if status == "healthy" else 503


@app.route("/metrics")
def metrics():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    boot_time = datetime.datetime.utcfromtimestamp(psutil.boot_time())

    return jsonify({
        "system": {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "boot_time": boot_time.isoformat() + "Z"
        },
        "cpu": {
            "usage_percent": cpu,
            "logical_cores": psutil.cpu_count(logical=True),
            "physical_cores": psutil.cpu_count(logical=False)
        },
        "memory": {
            "total_mb": round(memory.total / 1024 / 1024, 2),
            "used_mb": round(memory.used / 1024 / 1024, 2),
            "available_mb": round(memory.available / 1024 / 1024, 2),
            "usage_percent": memory.percent
        },
        "disk": {
            "total_gb": round(disk.total / 1024 / 1024 / 1024, 2),
            "used_gb": round(disk.used / 1024 / 1024 / 1024, 2),
            "free_gb": round(disk.free / 1024 / 1024 / 1024, 2),
            "usage_percent": disk.percent
        },
        "network": {
            "bytes_sent_mb": round(net.bytes_sent / 1024 / 1024, 2),
            "bytes_recv_mb": round(net.bytes_recv / 1024 / 1024, 2)
        },
        "app_uptime": get_uptime(),
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"Starting Flask Monitor App on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=debug)
