from flask import Flask
import psutil
import json
import subprocess

app = Flask(__name__)

@app.route('/cpu-usage')
def cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return json.dumps({'cpu_percent': cpu_percent})

@app.route('/ram-usage')
def ram_usage():
    ram_percent = psutil.virtual_memory().percent
    return json.dumps({'ram_percent': ram_percent})

@app.route('/gpu-usage')
def gpu_usage():
    try:
        # Run nvidia-smi command to get GPU utilization
        output = subprocess.check_output(["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"])
        gpu_utilization = float(output.decode().strip())
        return json.dumps({'gpu_percent': gpu_utilization})
    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on all available network interfaces
