from flask import Flask
import json
from read_json import *

app = Flask(__name__)

devices = [{'device_id': 0, 'patient_id': 5, 'measurement': 'temperature', 'data': {'unit': 'f', 'value': '100'}}, {'device_id': 1, 'patient_id': 5, 'measurement': 'oxygen level', 'data': {'unit': '%', 'value': 100}}]

@app.route('/')
def hello_world():
   return "Health-Care-API"

@app.route('/status/<int:device_id>', methods=['GET'])
def get(device_id):

   test = check_json(devices[device_id])
   return json.dumps(test)

if __name__ == "__main__":
   app.run(debug=True)