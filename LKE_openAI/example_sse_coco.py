import requests
import json
import uuid


def call_sse_api():
    url = "https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse"
    headers = {"Content-Type": "application/json"}

    payload = {
        "request_id": str(uuid.uuid4()),
        "content": "马化腾是谁",  # 修改提问内容
        "session_id": str(uuid.uuid4()),
        "bot_app_key": "QzmpGuMV",    #你的appkey
        "visitor_biz_id": str(uuid.uuid4())
    }

    try:
        response = requests.post(url, headers=headers, json=payload, stream=True)

        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            print(response.text)
            return

        current_content = ""  # 用于跟踪当前回复内容
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8').strip()

                # 解析事件类型
                if line_str.startswith('event:'):
                    event_type = line_str.split(':', 1)[1].strip()

                # 处理数据内容
                elif line_str.startswith('data:'):
                    data_str = line_str.split(':', 1)[1].strip()
                    try:
                        data = json.loads(data_str)

                        # 处理回复内容
                        if event_type == 'reply':
                            payload = data.get('payload', {})
                            new_content = payload.get('content', "")
                            is_final = payload.get('is_final', False)

                            # 更新并实时显示内容（带光标回退）
                            if new_content and new_content != current_content:
                                current_content = new_content
                            print(f"\r{current_content}", end="", flush=True)

                            # 最终换行结束
                            if is_final:
                                print("\n")

                            # 处理参考来源
                            elif event_type == 'reference':
                                references = data.get('payload', {}).get('references', [])
                                if references:
                                    print("\n\n参考资料：")
                                for idx, ref in enumerate(references, 1):
                                    print(f"{idx}. {ref.get('name', '未命名')}")
                                    print(f"   URL：{ref.get('url', '无有效链接')}\n")

                    except json.JSONDecodeError:
                        print(f"解析失败数据：{data_str}")

    except Exception as e:
        print(f"请求异常：{str(e)}")

if __name__ == "__main__":
    call_sse_api()