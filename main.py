from flask import Flask, request, jsonify
import psutil
import json
import subprocess

from Database import Database
from Routing import Routing

app = Flask(__name__)


if __name__ == '__main__':
    db = Database()
    Routing(app, db)
    app.run(host='0.0.0.0', port=5000)
