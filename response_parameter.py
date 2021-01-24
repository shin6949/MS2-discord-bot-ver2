import json


def get_param(middle, end):
    with open('./response_parameter_map.json', 'r') as file:
        json_data = json.load(file)

    file.close()
    return json_data[middle][end]

