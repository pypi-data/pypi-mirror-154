import os
import requests

def import_library(url, cache=True):
    file_name = url.split('/')[-1]
    import_id = file_name.split('.')[0]

    if not file_name in os.listdir() or not cache:
        response = requests.get(url)

        with open(file_name, 'w') as output_file:
            output_file.write(response.text)

    return __import__(import_id)