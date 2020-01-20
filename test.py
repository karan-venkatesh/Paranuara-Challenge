import json


with open('people.json') as f:
    d = json.load(f)
    print(type(d))
    for item in d:
        print(item)