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

character_list = response_parameter.get_param(service_name, 'character-list')
nickname_key = response_parameter.get_param(service_name, 'nickname')
rank = response_parameter.get_param(service_name, 'rank')
trophy = response_parameter.get_param(service_name, 'trophy')
profile_url = response_parameter.get_param(service_name, "profile-url")


def get_character(ctx, nickname):
    headers, body = cp.configure_request(ctx, request_mode)

    if nickname is None:
        url = f"{api.url}/trophy/character/firstpage/realtime?apitoken={api.apiToken}"
    else:
        url = f"{api.url}/trophy/character/realtime?apitoken={api.apiToken}&nickname={nickname}"
    response = cp.request_url(url, body, headers)

    return configure_message_one(response)


def configure_message_one(response):
    if response['error']:
        response.update({"log": response['msg']})
        return response

    if response[cp.status] == 'fail' and not response['error']:
        msg = "캐릭터를 찾지 못했습니다." + cp.add_admin_info(response[cp.process_time])
        response.update({"msg": msg, "log": msg})
        return response

    character = response[character_list][0]
    urllib.request.urlretrieve(character[profile_url], character[nickname_key] + ".png")

    r, g, b = image_processing.get_average(character[nickname_key])
    line_color = Colour.from_rgb(r, g, b)

    embed = discord.Embed(title="캐릭터 검색 결과", description="  ", color=line_color)
    embed.add_field(name="닉네임", value=character[nickname_key], inline=True)
    embed.add_field(name="순위", value="{}위".format(format(int(character[rank]), ",")), inline=True)
    embed.add_field(name="트로피", value="{}개".format(format(int(character[trophy]), ",")), inline=False)
    embed.set_thumbnail(url="attachment://profileimage.png")

    log = "캐릭터 검색 결과\n닉네임: {}\n순위: {}\n트로피: {}\n프로필 사진URL: {}" \
        .format(character[nickname_key], character[rank], character[trophy], character[profile_url])

    msg = str()
    if response[cp.admin]:
        msg = cp.add_admin_info(response[cp.process_time])
        log += cp.add_admin_info(response[cp.process_time])

    response.update({'error': False, 'log': log, 'embed': embed, 'msg': msg if response[cp.admin] else None})

    return response


async def send_message_one(result, channel):
    if result['error']:
        await channel.send(result['msg'], delete_after=30.0)
        return None

    if result[cp.ban] or result[cp.status] == "fail":
        return None

    character = result[character_list][0]
    file = discord.File(character[nickname_key] + ".png", filename="profileimage.png")

    if result[cp.admin]:
        await channel.send(result['msg'], embed=result['embed'], file=file)
    else:
        await channel.send(embed=result['embed'], file=file, delete_after=60.0)

    log.update_log(result[cp.log_num], result['log'])
    return None


async def send_message_first_page(result, chat):
    msg = str()

    for character in result[character_list]:
        rank_value = format(int(character.get(rank)), ",")
        name = character.get(nickname_key)
        trophy_value = format(int(character.get(trophy)), ",")

        msg += f"```[{rank_value}위] {name}\n트로피: {trophy_value}개```"

    if result[cp.admin]:
        await chat.edit(content=msg)
    else:
        await chat.edit(content=msg, delete_after=60.0)

    log.update_log(result[cp.log_num], msg)
    return None

