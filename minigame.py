import api_server_info as api
import discord
import common_process as cp
import log
import response_parameter

# 상수들 정의
request_mode = "mini"
service_name = 'minigame'

time = response_parameter.get_param(service_name, 'time')
first_game = response_parameter.get_param(service_name, 'first-game')
second_game = response_parameter.get_param(service_name, 'second-game')
pvp_game = response_parameter.get_param(service_name, 'pvp-game')


def get_now_minigame(message):
    headers, body = cp.configure_request(message, request_mode)

    url = "{}/minigame/now?apitoken={}".format(api.url, api.apiToken)
    response = cp.request_url(url, body, headers)

    return configure_message(response)


def get_next_minigame(message):
    headers, body = cp.configure_request(message, request_mode)

    url = "{}/minigame/next?apitoken={}".format(api.url, api.apiToken)
    response = cp.request_url(url, body, headers)

    return configure_message(response)


def configure_message(response):
    if response['error']:
        return response

    embed = discord.Embed(title="{} 미니게임".format(response[time]), description="  ", color=0x00ff56)
    embed.add_field(name="첫 번째 미니게임", value=response[first_game], inline=False)
    embed.add_field(name="두 번째 미니게임", value=response[second_game], inline=False)
    embed.add_field(name="PvP", value=response[pvp_game], inline=False)

    log = "{} 미니게임\n첫 번째 미니게임\n{}\n두 번째 미니게임\n{}\nPvP\n{}" \
        .format(response[time], response[first_game], response[second_game], response[pvp_game])

    msg = str()
    if response[cp.admin]:
        msg = cp.add_admin_info(response[cp.process_time])
        log += cp.add_admin_info(response[cp.process_time])

    response.update({'error': False, 'log': log, 'embed': embed, 'msg': msg if response[cp.admin] else None})

    return response


async def common_mini_processing(result, channel):
    if result['error']:
        await channel.send(result['msg'], delete_after=30.0)
        return None

    if result[cp.ban]:
        return None

    if result[cp.admin]:
        await channel.send(result['msg'], embed=result['embed'])
    else:
        await channel.send(result['msg'], embed=result['embed'], delete_after=60.0)

    log.update_log(result[cp.log_num], result['log'])
    return None

