import csv
import itertools
import json
import os.path
import time
import uuid

import requests
import sseclient
from flask import Flask, request, render_template, redirect, jsonify, url_for, Response
import session
from module.ticketParse import ticket_parse
from example_sse_coco import call_sse_api
from example_sse import sse_client
from module.taiji2 import hunyuan, moodifyflag, checkflag

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

data = []
json_data = ""
file_name = ""
json_prompt = ""
LLM_output = ""
prompt_num = 0
prompt_key = ""
origin_prompt = ""

ss_url = "http://stream-server-online-openapi.turbotke.production.polaris:8080/openapi/chat/completions"
model = "Hunyuan-T1-32K"
wsid = "10697"
enable_stream = True

headers = {
    "Content-Type": "application/json",
    # "Authorization": "0c370ac1-ba61-4b86-940a-f0ea8c05c680",
    "Authorization": "Bearer 7auGXNATFSKl7dF",
    "Wsid": wsid,
}


@app.route("/index", methods=['GET', 'POST'])
def index():
    global json_data
    global file_name
    global data
    global json_prompt
    global prompt_key
    global prompt_num
    global origin_prompt

    if request.method == 'POST':
        # file upload

        print(request.form.keys())

        if list(request.form.keys())[0] == 'file-upload-button' and len(list(request.files)):

            json_data, file_name, data = ticket_parse(APP_ROOT, request)

            prompt_num = len(data)
            for key in data[0].keys():
                prompt_key += key + "，"
            prompt_key = prompt_key[:-1]

            # origin_prompt = "假设你是一名腾讯云工程师，以上是2025年至今的EMR产品控制台及流程类问题的工单记录，共计" + str(prompt_num) + "单，他们是json的格式。\n\
            # 请你根据每个工单的" + prompt_key + "字段，分析并输出以上" + str(prompt_num) + "个工单的共性问题输出报告，报告中每个共性问题应当包含：\n\
            # 1. 具体单一的共性问题，不要模棱两可\n\
            # 2. 和本共性问题关联的工单，包含工单的问题和原因\n\
            # 3. 本共性问题的根因分析\n\
            # 4. 本共性问题可能的优化方向\n\
            # 并在回答最后，对报告中包含的多个共性问题进行表格的总结输出。\n"
            # json_prompt = json_data + "\n" + origin_prompt
            # json_prompt = origin_prompt
            print("json_prompt:\n" + json_prompt)


            return render_template('index.html', file_name=file_name, json_data=data, prompt_num=str(prompt_num), prompt_key=prompt_key, origin_prompt=origin_prompt), 200
        elif list(request.form.keys())[0] == 'analysis-button':

            print(request.form['analysis-button'])

            origin_prompt = request.form['analysis-button']

            json_prompt = json_data + "\n" + origin_prompt

            moodifyflag(True)

            return render_template('index.html', file_name=file_name, json_data=data, prompt_num=str(prompt_num), prompt_key=prompt_key, origin_prompt=origin_prompt), 200

    return render_template('index.html', json_data="")


@app.route('/stream')
def stream():
    if json_prompt != "" and checkflag():
        return Response(hunyuan(json_prompt), mimetype="text/event-stream")
    return render_template('index.html', file_name=file_name, json_data=data, origin_prompt=origin_prompt), 200


if __name__ == "__main__":
    session_id = session.get_session()
    app.run(port=5008, debug=True)
