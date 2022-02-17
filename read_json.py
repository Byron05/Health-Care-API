import json
import sys
import re

# Making a Global Variable for the required fields in the JSON file
FIELDS = ['device_id', 'patient_id', 'measurement', 'data']

# Making a global variable to act like the database to check if the device ID is in our system
DEVICES = [0,1,2,3,4,5]

def read_json(filename):
    
    # Open json file and read it
    with open(filename, 'r') as openfile:

        json_object = json.load(openfile)
    
    # Now check for validity
    flag = check_json(json_object)

    # If valid output to a .txt file
    if(flag):

        # Create a json file from the dictionary
        object = json.dumps(json_object, indent = 4)
  
        # Writing to sample.json
        with open("sample.txt", "w") as outfile:
            outfile.write(object)

        # with open('test.txt', 'w') as outfile:
        #     json.dump(json_object, outfile)

    # If invalid send an error
    else:
        print("Invalid JSON format")

def check_json(json):

    # Extract all the keys from the json object
    keys = list(json.keys())

    # First check if all the necessary fields exist
    if (FIELDS == keys):
        
        # Now we would have to check if the device id exists in our database
        # For now just using a global variable for this
        device_id = int(json['device_id'])
        if (device_id in DEVICES):

            if(measurements(json)):
                return True
    else:
        return False

def measurements(json):

    # Missing to do a try and catch block in case i cant convert unit
    # not checking if value contains letters or if units contains numbers
    name = json['measurement']
    unit = json['data']['unit']
    value = int(json['data']['value'])

    # Check that the units and values are correct
    if (name == "temperature"):

        # print("Temp")
        if ( (unit == 'k' or unit == 'c' or unit == 'f') and (value >= 0)):
            return True

    if (name == "blood pressure"):

        # print("Blood Press")
        if ( (unit == 'mmHg') and (value >= 0)):
            return True

    if (name == "heart beat"):

        # print("Heart Beat")
        if ( (unit == 'bpm') and (value >= 0)):
            return True

    if (name == "weight"):

        # print("Weight")
        if ( (unit == 'lbs') and (value >= 0)):
            return True
    
    if (name == "oxygen level"):

        # print("Oxygen Level")
        if ( (unit == 'percent') and (value >= 0)):
            return True

    else:
        # print("Two")
        return False


if __name__ == "__main__":

    # Getting the filename from the arguments passed
    filename = sys.argv[1]

    read_json(filename)








# {
#    "device_id" : "123",
#    "devive_info" : {
#       "device_name" : "thermometer",
#       "patient" : "Byron Mitchell",
#       "data" : {
#          "unit" : "f",
#          "temperature" : "100"
#       }
#    }   
# }