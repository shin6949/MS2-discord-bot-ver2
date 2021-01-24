import response_parameter
import requests
import json

# 공통 상수들
query = response_parameter.get_param('request', 'query')
call_value = response_parameter.get_param('request', 'call-value')
is_dm = response_parameter.get_param('request', 'is-dm')
user_id = response_parameter.get_param('request', 'user-id')
server_id = response_parameter.get_param('request', 'server-id')

ban = response_parameter.get_param('common', 'ban')
count = response_parameter.get_param('common', 'count')
admin = response_parameter.get_param('common', 'admin')
process_time = response_parameter.get_param('common', 'process-time')
log_num = response_parameter.get_param('common', 'log-num')


def add_admin_info(process_time):
    return "\n연산 소요 시간: {}ms".format(process_time)


def judge_status_code(status_code):
    if status_code == 200:
        return None
    elif status_code == 500:
        return "내부 서버 에러로 인해 정보를 받아올 수 없습니다."
    elif status_code == 401:
        return "내부 서버 인증 문제로 인해 정보를 받아올 수 없습니다."
    elif status_code == 400:
        return "올바르지 않은 값을 제출하여 서버에서 정보를 받아올 수 없습니다."
    else:
        return "내부 서버 에러로 인해 정보를 받아올 수 없습니다."


def request_url(url, body, headers):
    r = requests.get(url, data=json.dumps(body), headers=headers)
    response = json.loads(r.text)

    error_message = judge_status_code(r.status_code)
    response.update({"error": False if error_message is None else True, "msg": error_message})

    return response


def configure_request(message, mode):
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json'
    }

    body = {
        query: message.content,
        call_value: mode,
        is_dm: True if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>" else False,
        user_id: message.author.id,
        server_id: None if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>" else message.guild.id
    }

    return headers, body

