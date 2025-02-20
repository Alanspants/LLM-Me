import socketio
import tcloud.get_token as gt
import session

bot_app_key = ""  # 机器人密钥，不是BotBizId (从运营接口人处获取)
visitor_biz_id = "202403130001"  # 访客 ID（外部系统提供，需确认不同的访客使用不同的 ID）
secret_id = ""  # 填入腾讯云AKSK密钥(从腾讯云控制台获取)
secret_key = ""  # 填入腾讯云AKSK密钥(从腾讯云控制台获取)
streaming_throttle = 1  # 节流控制

tencent_cloud_domain = "tencentcloudapi.com"  # 腾讯云API域名
scheme = "https"  # 协议
req_method = "POST"  # 请求方法
region = "ap-guangzhou"  # 地域

conn_type_api = 5  # API 访客


def get_token():
    secret = {
        "secret_id": secret_id,
        "secret_key": secret_key
    }
    http_profile = {
        "domain": tencent_cloud_domain,
        "scheme": scheme,
        "method": req_method
    }
    params = {
        "Type": conn_type_api,
        "BotAppKey": bot_app_key,
        "VisitorBizId": visitor_biz_id
    }
    tk = gt.get_token(secret, http_profile, region, params)
    return tk


def start_conversation(url, path, ws_token: str):
    sio = socketio.SimpleClient()
    sio.connect(url=url,
                socketio_path=path,
                transports=["websocket"],
                auth={"token": ws_token})
    session_id = session.get_session()
    try:
        while True:
            content = input("请输入你想问的问题：")
            if content == "exit":
                exit(0)
            request_id = session.get_request_id()
            req_data = {"request_id": request_id, "content": content, "session_id": session_id}
            print(f'req_data:{req_data}')
            sio.emit("send", {"payload": req_data})
            while True:
                event = sio.receive()  # timeout单位：秒
                data = event[1]
                if event[0] == "reply":
                    if data["payload"]["is_from_self"]:  # 自己发出的包
                        print(f'is_from_self, event:{event[0]}, "content:"{data["payload"]["content"]}')
                    elif data["payload"]["is_final"]:  # 服务端event传输完毕；服务端的回复是流式的，最后一条回复的content，包含完整内容
                        print(f'is_final, event:{event[0]}, "content:"{data["payload"]["content"]}')
                        break
                else:
                    print(f'event:{event[0]}, "data:"{data}')
                    break
    except Exception as e:
        print(e)


if __name__ == "__main__":
    token = get_token()
    if token == "":
        print("get token error")
        exit(0)
    start_conversation("wss://wss.lke.cloud.tencent.com", "v1/qbot/chat/conn", token)
