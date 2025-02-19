# -*- coding: utf-8 -*-

import os
import time
import uuid
import json
import requests
import sseclient

# 服务组：Hunyuan-T1-32K
# WSID：10697
# Authorization：Bearer 7auGXNATFSKl7dF

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


def hunyuan(content):
    json_data = {
        "model": model,
        "query_id": "test_query_id_" + str(uuid.uuid4()),
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": content}
        ],
        "temperature": 1,
        "top_p": 0.8,
        "top_k": 40,
        "repetition_penalty": 1,
        "output_seq_len": 16000,
        "max_input_seq_len": 28000,
        "stream": enable_stream,
    }

    print('Input:\n{} | {} | {}'.format(ss_url, headers, json_data))
    resp = requests.post(ss_url, headers=headers, json=json_data, stream=True)

    print('Output:')
    if enable_stream:
        client = sseclient.SSEClient(resp)
        for event in client.events():
            if event.data != '':
                data_js = json.loads(event.data)
                try:
                    print(data_js['choices'][0]['delta']['content'], end='', flush=True)
                except Exception as e:
                    print(data_js)
    else:
        print(resp.json())
