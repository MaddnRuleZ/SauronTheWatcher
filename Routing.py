from flask import Flask, request, jsonify, g
import psutil
import json

class Routing:
    def __init__(self, app, store):
        self.app = app
        self.store = store
        self.register_routes()

    def register_routes(self):
        self.app.add_url_rule('/set', view_func=self.set_key_value, methods=['POST'])
        self.app.add_url_rule('/get', view_func=self.get_key_value, methods=['GET'])
        self.app.add_url_rule('/ram-usage', view_func=self.ram_usage)

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