import api_server_info as api
import discord
import common_process as cp
import log
import response_parameter as rp


# 상수들 정의
request_mode = 'boss'
service_name = 'boss'

boss_list = rp.get_param(service_name, "boss-list")
name_key = rp.get_param(service_name, "name")
level_key = rp.get_param(service_name, "level")
time_key = rp.get_param(service_name, "time")
map_key = rp.get_param(service_name, "map")
comment_key = rp.get_param(service_name, "comment")
even_time_boss_key = rp.get_param(service_name, "even-time-boss")


def _request(ctx, url):
    headers, body = cp.configure_request(ctx, request_mode)
    response = cp.request_url(url, body, headers)

    msg = cp.judge_status_code(response)
    if msg is None:
        response.update({'error': False})
    else:
        response.update({'error': True, 'msg': msg})

    return configure_message(response)


def get_bosses_soon(ctx):
    url = f"{api.url}/boss/soon?apitoken={api.apiToken}"

    return _request(ctx, url)


def get_bosses_next(ctx):
    url = f"{api.url}/boss/next?apitoken={api.apiToken}"

    return _request(ctx, url)


def get_bosses_by_name(ctx, keyword):
    url = f"{api.url}/boss/get-by-name?apitoken={api.apiToken}&name={keyword}"

    return _request(ctx, url)


def get_bosses_by_time(ctx, keyword):
    url = f"{api.url}/boss/get-by-time?apitoken={api.apiToken}&minute={keyword}"

    return _request(ctx, url)


def configure_message(response):
    msg = f"검색 결과: {len(response[boss_list])}개\n"

    if len(response[boss_list]) == 0:
        msg += "검색 결과가 없습니다."
    else:
        for boss in response[boss_list]:
            msg += f"```이름: {boss[name_key]}\n" \
                   f"등장 시간: {boss[time_key]}분\n" \
                   f"레벨: {boss[level_key]}\n" \
                   f"맵: {boss[map_key]}"

            # 연산자로는 개행이 불가함.
            if boss[comment_key] is None:
                msg += "```"
            else:
                msg += "\n" + boss[comment_key] + "```"

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

