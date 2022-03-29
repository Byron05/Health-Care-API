from flask import Flask, request, jsonify, Response, render_template, redirect, url_for, session
import bcrypt
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from read_json import *

app = Flask(__name__)
app.secret_key = "testing"
app.config["MONGO_URI"] = "mongodb+srv://byron:test@cluster0.dnlr5.mongodb.net/health-care-api?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Home Route
@app.route("/", methods=['post', 'get'])
def index():
   message = ''

   if "email" in session:
      return redirect(url_for("logged_in"))

   if request.method == "POST":

      usertype = request.form.get("usertype")
      usertype = usertype.lower()

      user = request.form.get("fullname")
      email = request.form.get("email")
      
      password1 = request.form.get("password1")
      password2 = request.form.get("password2")
      
      user_found = mongo.db.users.find_one({"name": user})
      email_found = mongo.db.users.find_one({"email": email})
      
      if usertype != "admin" and usertype != "patient":
         message = 'Please enter either Admin or Patient'
         return render_template('index.html', message=message)

      if user_found:
         message = 'There already is a user by that name'
         return render_template('index.html', message=message)

      if email_found:
         message = 'This email already exists in database'
         return render_template('index.html', message=message)

      if password1 != password2:
         message = 'Passwords should match!'
         return render_template('index.html', message=message)

      else:
         hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
         user_input = {'usertype': usertype, 'name': user, 'email': email, 'password': hashed}
         mongo.db.users.insert_one(user_input)
         
         user_data = mongo.db.users.find_one({"email": email})
         new_email = user_data['email']

         #return render_template('logged_in.html', email=new_email)
         return redirect(url_for("login"))
         #return render_template('login.html', message="Registration Successful, Please Login!")

   return render_template('index.html')


# Already logged in
@app.route('/logged_in')
def logged_in():

   if "name" in session:
      name = session["name"]
      return render_template('logged_in.html', name=name)

   else:
      return redirect(url_for("login"))


# Login Route
@app.route("/login", methods=["POST", "GET"])
def login():

   message = 'Please login to your account'

   if "email" in session:
      return redirect(url_for("logged_in"))
   
   if request.method == "POST":

      email = request.form.get("email")
      password = request.form.get("password")

      email_found = mongo.db.users.find_one({"email": email})
      if email_found:

         usertype = email_found['usertype']
         name = email_found['name']
         email_val = email_found['email']
         passwordcheck = email_found['password']
         
         if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):

            session['usertype'] = usertype
            session['name'] = name
            session["email"] = email_val
            return redirect(url_for('logged_in'))

         else:

            if "email" in session:
               return redirect(url_for("logged_in"))

            message = 'Wrong password'
            return render_template('login.html', message=message)

      else:

         message = 'Email not found'
         return render_template('login.html', message=message)

   return render_template('login.html', message=message)


# Logout Route
@app.route("/logout", methods=["POST", "GET"])
def logout():

   if "email" in session:
      session.pop("email", None)
      session.pop("name", None)
      session.pop("usertype", None)
      return render_template("signout.html")

   else:
      return render_template('index.html')


# Route For Admins Only
# Create new measurement entry
@app.route("/create", methods=["POST", "GET"])
def create():
   
   message = 'Enter Measurement Info'

   if request.method == "POST":
      
      device_id = int(request.form.get("device_id"))
      patient_id = int(request.form.get("patient_id"))
      measurement = request.form.get("measurement")
      unit = request.form.get("unit")
      value = int(request.form.get("value"))

      content = {'device_id': device_id, 'patient_id': patient_id, 'measurement': measurement, 'data': {'unit': unit, 'value': value }}

      flag, message = check_json(content)

      if flag:
         
         mongo.db.devices.insert_one(content)
         return render_template('logged_in.html', name=session["name"], message="Entry was successful!")

      else:

         return render_template('measurement.html', message=message)

   return render_template('measurement.html', message=message)


# send message 
@app.route("/send", methods=["POST", "GET"])
def send():
   
   message = 'Enter Message Info'

   if request.method == "POST":
      
      recipient = request.form.get("recipient")
      # sender = request.form.get("from")
      sender = session["name"]
      message = request.form.get("message")

      content = {'To': recipient, 'From': sender, 'Message': message}

      if (mongo.db.users.find_one({'name': recipient})):

         mongo.db.messages.insert_one(content)
         return render_template('logged_in.html', name=session["name"], message="Message Sent!")

      else:

         return render_template('messages.html', message="Recipient doesn't exist")

   return render_template('messages.html', message=message)







# Route to get all measurements in the database
@app.route('/measurements', methods=['GET'])
def get_measurements():

   measurements = mongo.db.devices.find()
   response = json_util.dumps(measurements)

   return Response(response, mimetype='application/json')


# Route to get a singular measurement using the id provided by mongodb
@app.route('/measurements/<id>', methods=['GET'])
def get_messurement(id):

   measurement = mongo.db.devices.find_one({'_id': ObjectId(id)})

   if (measurement == None):
      return not_found()

   response = json_util.dumps(measurement)

   return Response(response, mimetype='application/json')


# Route to delete all measurements in the data base
@app.route('/measurements', methods=['DELETE'])
def delete_measurements():

   measurements = mongo.db.devices.delete_many({})
   response = jsonify({'message': str(measurements.deleted_count) + " documents deleted"})
   
   return response


# Route to delete a specific measurement using the id provided by mongodb
@app.route('/measurements/<id>', methods=['DELETE'])
def delete_measurement(id):
   measurement = mongo.db.devices.find_one({'_id': ObjectId(id)})

   if (measurement == None):
      return not_found()

   measurement = mongo.db.devices.delete_many({})
   response = jsonify({'message': 'Measurement ' + id + ' was Deleted successfully'})

   return response


# Route to update a specific measurement using the id provided by mongodb
@app.route('/measurements/<id>', methods=['PUT'])
def update_measurement(id):
   
   measurement = mongo.db.devices.find_one({'_id': ObjectId(id)})

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

      mongo.db.devices.update_one({'_id': ObjectId(id)}, {'$set': {
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

      id = mongo.db.devices.insert_one(content)

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
