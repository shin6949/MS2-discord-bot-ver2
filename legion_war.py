import api_server_info as api
import common_process as cp
import log
import response_parameter as rp


# 상수들 정의
request_mode = 'legion'
service_name = 'legion'

legion_war_list = rp.get_param(service_name, "legion-war-list")
name_key = rp.get_param(service_name, "name")
even_time_key = rp.get_param(service_name, "even-time")


def __request(ctx, url):
    headers, body = cp.configure_request(ctx, request_mode)
    response = cp.request_url(url, body, headers)

    msg = cp.judge_status_code(response)
    if msg is None:
        response.update({'error': False})
    else:
        response.update({'error': True, 'msg': msg})

    return configure_message(response)


def get_legion_war_soon(ctx):
    url = f"{api.url}/legion/soon?apitoken={api.apiToken}"

    return __request(ctx, url)


def get_legion_war_next(ctx):
    url = f"{api.url}/legion/next?apitoken={api.apiToken}"

    return __request(ctx, url)


def configure_message(response):
    msg = "군단전 정보입니다.\n"

    for legion_war in response[legion_war_list]:
        msg += f"```이름: {legion_war[name_key]}\n" \
               f"등장 시간: {'짝수 시 50분' if legion_war[even_time_key] is True else '홀수 시 50분'}```"

    if response[cp.admin]:
        msg += cp.add_admin_info(response[cp.process_time])

    response.update({'error': False, 'msg': msg})

    return response


async def send_message(result, chat):
    msg = result['msg']

    if result[cp.admin]:
        await chat.edit(content=msg)
    else:
        await chat.edit(content=msg, delete_after=60.0)

    log.update_log(result[cp.log_num], msg)
    return None

