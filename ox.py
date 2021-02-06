import requests
import json
from discord.ext import commands

# 별도 파일들
import api_server_info
import log
import common_process as cp
import response_parameter

# 상수들 정의
mode = response_parameter.get_param('ox', 'mode')
problem_list = response_parameter.get_param('ox', 'problem-list')
answer = response_parameter.get_param('ox', 'answer')
question = response_parameter.get_param('ox', 'question')


def configure_msg(response, result, keyword):
    if result.get(cp.ban):
        return result

    msg = "\'{}\'에 대한 {} 결과: {}개".format(keyword, response[mode], response[cp.count])

    if response[cp.count] == 0:
        msg = "\"{}\"에 대한 검색 결과가 없습니다.\n제보는 '!제보'".format(keyword)
        if response[cp.admin]:
            msg += cp.add_admin_info(response[cp.process_time])
        result.update({'msg': msg})
        return result

    if response[cp.count] >= 30:
        msg = "\"{}\"에 대한 검색 결과가 30개가 넘어요!\n디스코드 내 최대 글자수 제한이 있어서 결과를 표시 할 수 없습니다. 좀 더 길게 검색해보세요.".format(keyword)
        if response[cp.admin]:
            msg += cp.add_admin_info(response[cp.process_time])
        result.update({'msg': msg})
        return result

    for problem in response[problem_list]:
        if problem[answer]:
            msg += ("```ini\n[O] {}\n```".format(problem[question]))
        else:
            msg += ("```\n[X] {}```".format(problem[question]))

    if response[cp.admin]:
        msg += cp.add_admin_info(response[cp.process_time])

    result.update({'msg': msg})
    return result


def get_ox(message, keyword):
    headers, body = configure_default_data(message)

    url = "{}/ox/search?apitoken={}&keyword={}".format(api_server_info.url, api_server_info.apiToken, keyword)
    response, result = request_url(url, body, headers)

    return configure_msg(response, result, keyword)


def get_ox_short(message, keyword):
    headers, body = configure_default_data(message)

    url = "{}/ox/search/short?apitoken={}&keyword={}".format(api_server_info.url, api_server_info.apiToken, keyword)
    response, result = request_url(url, body, headers)

    return configure_msg(response, result, keyword)


def request_url(url, body, headers):
    r = requests.get(url, data=json.dumps(body), headers=headers)
    response = json.loads(r.text)

    error_message = cp.judge_status_code(r.status_code)
    if error_message is None:
        result = {'error': False, cp.ban: response[cp.ban],
                  cp.admin: response[cp.admin], cp.log_num: response[cp.log_num]}
    else:
        result = {'error': True, 'msg': error_message}

    return response, result


def configure_default_data(message):
    headers, body = cp.configure_request(message, "ox")

    return headers, body


async def common_ox_processing(result, channel):
    if result['error']:
        await channel.send(result['msg'], delete_after=30.0)
        return None

    if result[cp.ban]:
        return None

    if result[cp.admin]:
        await channel.send(result['msg'])
    else:
        await channel.send(result['msg'], delete_after=60.0)

    log.update_log(result[cp.log_num], None if result[cp.ban] else result['msg'])
    return None

