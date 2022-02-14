import json
import sys
import re

filename = sys.argv[1]

with open(filename, 'r') as openfile:

    json_object = json.load(openfile)

print(json_object)
print(type(json_object))