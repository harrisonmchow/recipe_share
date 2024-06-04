import json

with open('../vue-frontend/src/assets/world-110m.json', 'r') as file:
    data = json.load(file)
    
array = data['objects']['countries']['geometries']
countriesList = []
for country in array:
    countriesList.append(country['properties']['name'])
    
obj = {'countries': countriesList}
json_obj = json.dumps(obj, indent=4)

with open('../vue-frontend/src/assets/countries.json', 'w') as file2:
    file2.write(json_obj)