# -*- coding: utf-8 -*-

import os
import time
import uuid
import json
import requests
import sseclient

ss_url = "http://stream-server-online-openapi.turbotke.production.polaris:81/openapi/chat/completions"
model = "DeepSeek-R1"
wsid = "10697"
enable_stream = True

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer 7auGXNATFSKl7dF",
    "Wsid": wsid,
}

json_data = {
    "model": model,
    "query_id": "test_query_id_" + str(uuid.uuid4()),
    "messages": [
      {"role": "system", "content": ""},
      {"role": "user", "content": "请输出1+1=2"}
    ],
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 40,
    "repetition_penalty": 1,
    "output_seq_len": 1024,
    "max_input_seq_len": 2048,
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
              if 'event' in data_js:
                  if data_js['event'].get('name', '') == 'thinking' and data_js['event'].get('state', -1) == 0:
                    print('开始思考')
                    continue
                  elif data_js['event'].get('name', '') == 'thinking' and data_js['event'].get('state', -1) == 2:
                    print('\n结束思考')
                    continue

              print(data_js)
else:
  print(resp.text)
