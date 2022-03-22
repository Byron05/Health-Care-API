from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from read_json import *

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://byron:test@cluster0.dnlr5.mongodb.net/devices?retryWrites=true&w=majority"

mongo = PyMongo(app)

# Home Route
@app.route('/')
def hello_world():
   return "Health-Care-API"

# Route to get all measurements in the data base
@app.route('/measurements', methods=['GET'])
def get_measurements():
   measurements = mongo.db.measurements.find()
   response = json_util.dumps(measurements)
   return Response(response, mimetype='application/json')

# Route to get a singular measurement using the id provided by mongodb
@app.route('/measurements/<id>', methods=['GET'])
def get_messurement(id):
   measurement = mongo.db.measurements.find_one({'_id': ObjectId(id)})

   if (measurement == None):
      return not_found()

   response = json_util.dumps(measurement)

   return Response(response, mimetype='application/json')

# Route to delete all measurements in the data base
@app.route('/measurements', methods=['DELETE'])
def delete_measurements():

   measurements = mongo.db.measurements.delete_many({})
   response = jsonify({'message': str(measurements.deleted_count) + " documents deleted"})
   
   return response

# Route to delete a specific measurement using the id provided by mongodb
@app.route('/measurements/<id>', methods=['DELETE'])
def delete_measurement(id):
   measurement = mongo.db.measurements.find_one({'_id': ObjectId(id)})

   if (measurement == None):
      return not_found()

   measurement = mongo.db.measurements.delete_many({})
   response = jsonify({'message': 'Measurement ' + id + ' was Deleted successfully'})

   return response

# Route to update a specific measurement using the id provided by mongodb
@app.route('/measurements/<id>', methods=['PUT'])
def update_measurement(id):
   
   measurement = mongo.db.measurements.find_one({'_id': ObjectId(id)})

   if (measurement == None):
      return not_found()
   
   # Receiving Data
   content = request.get_json()

   #check that json is in the correct format
   flag, message = check_json(content)

   if flag:

      device_id = request.json['device_id']
      patient_id = request.json['patient_id']
      measurement = request.json['measurement']
      unit = request.json['data']['unit']
      value = request.json['data']['value']

      mongo.db.measurements.update_one({'_id': ObjectId(id)}, {'$set': {
         'device_id': device_id,
         'patient_id': patient_id,
         'measurement': measurement,
         'data': {
            'unit': unit,
            'value': value
         }
      }})

      response = jsonify({'message': 'Measurement ' + id + ' was upadated successfully'})
      return response
   
   else:
      return not_found(message)


# Route to receive and post a json object if it is a valid json
@app.route('/measurements', methods=['POST'])
def create_measurement():
   
   # Receiving Data
   content = request.get_json()

   #check that json is in the correct format
   flag, message = check_json(content)

   if flag:

      id = mongo.db.measurements.insert_one(content)

      device_id = request.json['device_id']
      patient_id = request.json['patient_id']
      measurement = request.json['measurement']
      unit = request.json['data']['unit']
      value = request.json['data']['value']

      response = jsonify({'id': str(id), 'device_id': device_id, 'patient_id': patient_id, 'measurement': measurement, 'data': {'unit': unit, 'value': value }})

      return response

   else:
      return not_found(message)

@app.errorhandler(404)
def not_found(message):
   
   if not message:

      response = jsonify({'message': 'Resource Not Found ' + request.url, 'status' : 404})
      response.status_code = 404

   else:
      response = jsonify({'message': message, 'status' : 1})
      response.status_code = 404

   return response

if __name__ == "__main__":
   app.run(debug=True)
