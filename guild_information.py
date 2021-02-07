from discord import Colour
import api_server_info as api
import discord
import common_process as cp
import urllib.request
import log
import response_parameter
import image_processing


# 상수들 정의
request_mode = 'trophy'
service_name = 'crawling-service'

guild_list = response_parameter.get_param(service_name, 'guild-list')
guild_name_string = response_parameter.get_param(service_name, 'guild-name')
rank = response_parameter.get_param(service_name, 'rank')
trophy = response_parameter.get_param(service_name, 'trophy')
profile_url = response_parameter.get_param(service_name, "profile-url")
master = response_parameter.get_param(service_name, 'master')


def get_guild(ctx, guild_name):
    headers, body = cp.configure_request(ctx, request_mode)

    if guild_name is None:
        url = f"{api.url}/trophy/guild/firstpage/realtime?apitoken={api.apiToken}"
    else:
        url = f"{api.url}/trophy/guild/realtime?apitoken={api.apiToken}&guildname={guild_name}"
    response = cp.request_url(url, body, headers)

    return configure_message_one(response)


def configure_message_one(response):
    if response['error']:
        response.update({"log": response['msg']})
        return response

    if response[cp.status] == 'fail' and not response['error']:
        msg = "길드를 찾지 못했습니다." + cp.add_admin_info(response[cp.process_time])
        response.update({"msg": msg, "log": msg})
        return response

    guild = response[guild_list][0]
    urllib.request.urlretrieve(guild[profile_url], guild[guild_name_string] + ".png")

    r, g, b = image_processing.get_average(guild[guild_name_string])
    line_color = Colour.from_rgb(r, g, b)

    embed = discord.Embed(title="길드 검색 결과", description="  ", color=line_color)
    embed.add_field(name="길드명", value=guild[guild_name_string], inline=True)
    embed.add_field(name="순위", value="{}위".format(format(int(guild[rank]), ",")), inline=True)
    embed.add_field(name="길드장", value=f"{guild[master]}", inline=True)
    embed.add_field(name="트로피", value="{}개".format(format(int(guild[trophy]), ",")), inline=False)
    embed.set_thumbnail(url="attachment://profileimage.png")

    log = f"길드 검색 결과\n" \
          f"길드명: {guild[guild_name_string]}\n" \
          f"순위: {guild[rank]}\n" \
          f"트로피: {guild[trophy]}\n" \
          f"길드장:{guild[master]}\n" \
          f"아이콘URL: {guild[profile_url]}" \

    msg = str()
    if response[cp.admin]:
        msg = cp.add_admin_info(response[cp.process_time])
        log += cp.add_admin_info(response[cp.process_time])

    response.update({'error': False, 'log': log, 'embed': embed, 'msg': msg if response[cp.admin] else None})

    return response


async def send_message_one(result, channel):
    """
    단일 검색 결과에 대한 값을 전송하는 함수. 파일 첨부가 필요하여, 수정 형태로 구현할 수 없음.

    :param result: API Server에서 받아온 JSON (Dict)
    :param channel: 전송할 Discord Channel 객체
    :return: None
    """
    if result['error']:
        await channel.send(content=result['msg'], delete_after=30.0)
        return None

    if result[cp.ban] or result[cp.status] == "fail":
        return None

    guild = result[guild_list][0]
    file = discord.File(guild[guild_name_string] + ".png", filename="profileimage.png")

    if result[cp.admin]:
        await channel.send(content=result['msg'], embed=result['embed'], file=file)
    else:
        await channel.send(embed=result['embed'], file=file, delete_after=60.0)

    log.update_log(result[cp.log_num], result['log'])
    return None


async def send_message_first_page(result, chat):
    """
    길드 1페이지에 대한 값을 리턴하는 함수.

    :param result: API Server에서 받아온 JSON (Dict)
    :param chat: 수정할 기존 Chat 객체
    :return: None
    """
    msg = str()
    for guild in result[guild_list]:
        rank_value = format(int(guild.get(rank)), ",")
        name = guild.get(guild_name_string)
        trophy_value = format(int(guild.get(trophy)), ",")
        master_value = guild.get(master)

        msg += f"```[{rank_value}위] {name}\n길드장:{master_value}\n길드 트로피: {trophy_value}개```"

    if result[cp.admin]:
        await chat.edit(content=msg)
    else:
        await chat.edit(content=msg, delete_after=60.0)

    log.update_log(result[cp.log_num], msg)
    return None

