import csv
import json
import os.path

from flask import Flask, request, render_template, session, redirect, jsonify, url_for

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# <form action="" method="post" id='myForm'>
#     <button name="button" value="value">Send</button>
# </form>
#
# <form action="" method="post" id='myForm2'>
#     <button id="myButton2" name="button2" value=0 onclick="modifyData()">Send</button>
# </form>
#
# <script>
#     function modifyData() {
#         data = "I want to send this to backend"
#         document.getElementById("myButton2").value = data;
#     }
# </script>

# @app.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         if list(request.form.keys())[0] == 'button':
#             print(request.form['button'])
#
#         if list(request.form.keys())[0] == 'button2':
#             print(request.form['button2'])
#
#     return render_template("index.html")


@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # file upload
        if list(request.form.keys())[0] == 'file-upload-button' and len(list(request.files)):

            file = request.files['file']
            file_list = list(request.files.values())
            file_name = file_list[0].filename
            print("file: " + str(file) + "\nfile_list: " + str(file_list) + "\nfile_name: " + str(file_name))

            target = os.path.join(APP_ROOT, "datasource/")
            destination = '/'.join([target, file_name])
            file.save(destination)

            csv_file_path = destination

            data = []
            with open(csv_file_path, encoding='utf_8_sig') as csvf:
                csv_reader = csv.DictReader(csvf)
                for row in csv_reader:
                    data.append(row)

            json_data = json.dumps(data, indent=4, ensure_ascii=False)
            print(type(json_data))
            print(type(data))

            return render_template('index.html', file_name=file_name, json_data=data), 200

    return render_template('index.html', json_data="")


if __name__ == "__main__":
    app.run(port=5000)
