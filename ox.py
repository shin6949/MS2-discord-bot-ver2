import requests
import json
import api_server_info


def configure_msg(response, result, keyword):
    msg = str()

    if result.get('ban'):
        return result

    if response['in-order']:
        msg += "\'{}\'에 대한 순차 검색 결과: {}개\n".format(keyword, response['count'])
    else:
        msg += "\'{}\'에 대한 비순차 검색 결과: {}개\n".format(keyword, response['count'])

    if response['count'] == 0:
        msg = "\"{}\"에 대한 검색 결과가 없습니다.\n제보는 '!제보'".format(keyword)
        if response['admin']:
            msg += add_admin_info(response['process_time'])
        result.update({'msg': msg})
        return result

    if response['count'] > 30:
        msg = "\"{}\"에 대한 검색 결과가 30개가 넘어요!\n디스코드 내 최대 글자수 제한이 있어서 결과를 표시 할 수 없습니다. 좀 더 길게 검색해보세요.".format(keyword)
        if response['admin']:
            msg += add_admin_info(response['process_time'])
        result.update({'msg': msg})
        return result

    for problem in response['problems']:
        if problem['answer']:
            msg += ("```ini\n[O] {}\n```".format(problem['question']))
        else:
            msg += ("```\n[X] {}```".format(problem['question']))

    if response['admin']:
        msg += add_admin_info(response['process_time'])

    result.update({'msg': msg})
    return result


def get_ox(message, keyword):
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json'
    }

    body = {
        "query": message.content,
        "callValue": "ox",
        "isDm": True if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>" else False,
        "userId": message.author.id,
        "serverId": None if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>" else message.guild.id
    }

    params = {
        'apitoken': api_server_info.apiToken,
        'keyword': keyword
    }

    url = "{}/ox/search".format(api_server_info.url)
    r = requests.get(url, data=json.dumps(body), params=params, headers=headers)
    response = json.loads(r.text)

    result = {'ban': response['is-ban'], 'admin': response['admin'], 'query-num': response['query-num']}

    return configure_msg(response, result, keyword)


def get_ox_short(message, keyword):
    pass


def add_admin_info(process_time):
    return "\n연산 소요 시간: {}ms".format(process_time)
