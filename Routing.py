from flask import Flask, request, jsonify, g
import psutil
import json
import subprocess
class Routing:
    def __init__(self, app, store):
        self.app = app
        self.store = store
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule('/set', view_func=self.set_key_value, methods=['POST'])
        self.app.add_url_rule('/get', view_func=self.get_key_value, methods=['GET'])
        self.app.add_url_rule('/ram-usage', view_func=self.ram_usage)
        self.app.add_url_rule('/cpu-usage', view_func=self.cpu_usage)
        self.app.add_url_rule('/gpu-usage', view_func=self.gpu_usage)

    def set_key_value(self):
        data = request.json
        key = data.get('key')
        value = data.get('value')
        if not key or not value:
            return jsonify({'error': 'Key and value are required'}), 400
        self.store.set_key_value('ItemKeyValueStore', key, value)
        return jsonify({'message': 'Key-Value pair set successfully'})

    def get_key_value(self):
        key = request.args.get('key')
        if not key:
            return jsonify({'error': 'Key is required'}), 400
        value = self.store.get_value_key_value_store('ItemKeyValueStore', key)
        if value is None:
            return jsonify({'error': 'Key not found'}), 404
        return jsonify({'key': key, 'value': value})

    def ram_usage(self):
        ram_percent = psutil.virtual_memory().percent
        return json.dumps({'ram_percent': ram_percent})

    def cpu_usage(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        return json.dumps({'cpu_percent': cpu_percent})

    def gpu_usage(self):
        try:
            output = subprocess.check_output(
                ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv,noheader,nounits"])
            gpu_utilization = float(output.decode().strip())
            return json.dumps({'gpu_percent': gpu_utilization})
        except Exception as e:
            return json.dumps({'error': str(e)})
