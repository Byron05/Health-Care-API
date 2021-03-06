import json
import sys

# Making a Global Variable for the required fields in the JSON file
FIELDS = ['device_id', 'patient_id', 'measurement', 'data']

# Making a global variable to act like the database to check if the device ID is in our system
DEVICES = [0, 1, 2, 3, 4, 5]


def read_json(filename):

    message = ""

    # Open json file and read it
    try:

        with open(filename, 'r') as openfile:

            json_object = json.load(openfile)
    except:
        message = "Error: Can't open JSON"
        return False, message

    else:

        # Now check for validity
        flag, message = check_json(json_object)

        # If valid output to a .txt file
        if(flag):

            # Create a json file from the dictionary
            object = json.dumps(json_object, indent=4)

            # Writing to sample.json
            with open("sample.txt", "w") as outfile:
                outfile.write(object)

            outfile.close()

            message = "Everything Good!"
            return True, message
            # with open('test.txt', 'w') as outfile:
            #     json.dump(json_object, outfile)

        # If invalid send an error
        else:
            message = "Invalid JSON format: " + message
            return False, message


def check_json(json):

    message = "Everything Successful"

    # Extract all the keys from the json object
    keys = list(json.keys())

    # First check if all the necessary fields exist
    if (FIELDS == keys):

        # Now we would have to check if the device id exists in our database
        # For now just using a global variable for this
        device_id = json['device_id']
        
        if (device_id in DEVICES and isinstance(device_id, int)):

            flag, message = check_fields(json)

            if(flag):
                return True, message
            else:
                return False, message
        else:
            message = "Device ID doesn't exist/wrong data type"
            return False, message
    else:
        message = "Incorrect JSON format"
        return False, message


def check_fields(json):

    # Missing to do a try and catch block in case i cant convert unit
    # not checking if value contains letters or if units contains numbers
    name = json['measurement']
    unit = json['data']['unit']
    value = json['data']['value']

    message = "Everything Successful"

    # Check that name, unit and value are their correct type (str or int)
    if (isinstance(name, int) or isinstance(unit, int) or isinstance(value, str)):
        message = "Incorrect data type for fields"
        return False, message

    # Check that the units and values are correct
    if (name == "temperature"):

        # print("Temp")
        if ((unit == 'k' or unit == 'c' or unit == 'f') and (value >= 0)):
            return True, message

    if (name == "blood pressure"):

        # print("Blood Press")
        if ((unit == 'mmHg') and (value >= 0)):
            return True, message

    if (name == "heart beat"):

        # print("Heart Beat")
        if ((unit == 'bpm') and (value >= 0)):
            return True, message

    if (name == "weight"):

        # print("Weight")
        if ((unit == 'lbs') and (value >= 0)):
            return True, message

    if (name == "oxygen level"):

        # print("Oxygen Level")
        if ((unit == 'percent' or unit == "%") and (value >= 0 and value <= 100)):
            return True, message

    else:
        message = "Measurement doesn't exist"
        return False, message

def create_json(json):

    device_id = json['device_id']
    patient_id = json['patient_id']
    measurement = json['measurement']
    unit = json['data']['unit']
    value = json['data']['value']

    response = {'device': {'device_id': device_id, 'patient_id': patient_id, 'measurement': measurement, 'data': {'unit': unit, 'value': value}}}
    
    return response


if __name__ == "__main__":

    # Getting the filename from the arguments passed
    filename = sys.argv[1]

    print(read_json(filename))
