import requests
import json

# 별도 파일들
import api_server_info as api
import log
import common_process as cp
import response_parameter

# 공통 상수들
query = response_parameter.get_param('request', 'query')
call_value = response_parameter.get_param('request', 'call-value')
is_dm = response_parameter.get_param('request', 'is-dm')
user_id = response_parameter.get_param('request', 'user-id')
server_id = response_parameter.get_param('request', 'server-id')

request_name = 'custom'
service_name = 'custom-message'
message_list = response_parameter.get_param(service_name, "message-list")
command_key = response_parameter.get_param(service_name, "command")
response_key = response_parameter.get_param(service_name, "response")
is_for_one_server = response_parameter.get_param(service_name, "is-for-one-server")


def configure_request(message):
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json'
    }

    body = {
        query: message.content,
        call_value: "custom",
        is_dm: True if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>" else False,
        user_id: message.author.id,
        server_id: None if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>" else message.guild.id
    }

    return headers, body


def get_custom_message(message):
    headers, body = configure_request(message)
    url = f"{api.url}/message/get?apitoken={api.apiToken}"

    r = requests.get(url, data=json.dumps(body), headers=headers)
    response = json.loads(r.text)

    error_message = cp.judge_status_code(r.status_code)
    if error_message is None:
        response.update({'error': False})
    else:
        response.update({'error': True, 'msg': error_message})

    return response


async def send_msg(channel, result):
    if result['count'] == 0:
        return None

    if result['error']:
        await channel.send(content=result['msg'], delete_after=30.0)
        return None

    if result[cp.ban]:
        return None

    msg = str()
    for message in result[message_list]:
        msg += message[response_key]

    if result[cp.admin]:
        msg += cp.add_admin_info(result['process-time'])
        await channel.send(content=msg)
    else:
        await channel.send(content=msg, delete_after=60.0)

    log.update_log(result[cp.log_num], None if result[cp.ban] else msg)
    return None

