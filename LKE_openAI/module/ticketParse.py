import csv
import json
import os


def ticket_parse(app_root, request):
    json_data = None
    file_name = None
    data = []

    file = request.files['file']
    file_list = list(request.files.values())
    file_name = file_list[0].filename
    print("file: " + str(file) + "\nfile_list: " + str(file_list) + "\nfile_name: " + str(file_name))

    target = os.path.join(app_root, "datasource/")
    destination = '/'.join([target, file_name])
    file.save(destination)

    csv_file_path = destination

    with open(csv_file_path, encoding='utf_8_sig') as csvf:
        csv_reader = csv.DictReader(csvf)
        for row in csv_reader:
            data.append(row)

    json_data = json.dumps(data, indent=4, ensure_ascii=False)

    return json_data, file_name, data
