import requests
import api_server_info
import json
import time

while 1:
    # 웹 서버가 계속 작동하도록 리퀘스트를 보냄.
    url = "{}/main".format(api_server_info.url)
    r = requests.get(url)
    response = r.text
    time.sleep(30)
