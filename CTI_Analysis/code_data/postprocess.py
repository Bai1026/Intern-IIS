import os
import csv
import json

input_folder = './json_file'
output_folder = './csv_file'

# go through all the files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        json_file_path = os.path.join(input_folder, filename)

        # read the json file
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        rows = []
        for sentence in data['sentences']:
            text = sentence['text']
            mappings = sentence['mappings']
            attack_ids = [mapping['attack_id'] for mapping in mappings]
            for attack_id in attack_ids:
                rows.append([text, attack_id])

        csv_filename = f'{os.path.splitext(filename)[0]}.csv'
        output_file_path = os.path.join(output_folder, csv_filename)

        with open(output_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Text', 'Attack ID']) 
            writer.writerows(rows)  

