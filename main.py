from flask import Flask
import psutil
import json

app = Flask(__name__)

@app.route('/cpu-usage')
def cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    return json.dumps({'cpu_percent': cpu_percent})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on all available network interfaces
