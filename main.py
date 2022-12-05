import Schedule
import PrimitiveJSONParser
import PrimitiveXMLParser
import PrimitiveYAMLParser
import RegJSONParser
import requests
import re
import time

import yaml
import json
import csv
from yaml.loader import SafeLoader

s = Schedule.Schedule("P3133")
Schedule.convertToJSON(s, "Вторник")
file = open ("Schedule.json", "r")
text = file.read()
file.close()
p = PrimitiveJSONParser.deserialize(text)
file = open("Schedule.csv", "w")
count = 0
text = ""
t = p["Lesson"]
for i in t:
    if count == 0:
        header = i.keys()
        for j in header:
            for k in i[j].keys():
                text += j + "/" + k + ","
        text = text[ : len(text) - 1]
        text += "\n"
        count += 1
    for j in i.keys():
        for k in i[j].keys():
            text += "\"" + i[j][k] + "\"" + ","
    text = text[ : len(text) - 1]
    text += "\n"
text = text[ : len(text) - 1]
file.write(text)
file.close()
