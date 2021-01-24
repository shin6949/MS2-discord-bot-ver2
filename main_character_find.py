import api_server_info as api
import discord
import common_process as cp
import urllib.request
import log
import response_parameter

# 상수들 정의
request_mode = 'trophy'
service_name = 'crawling-service'

character_list = response_parameter.get_param(service_name, 'character-list')
nickname = response_parameter.get_param(service_name, 'nickname')
rank = response_parameter.get_param(service_name, 'rank')
trophy = response_parameter.get_param(service_name, 'trophy')
profile_url = response_parameter.get_param(service_name, "profile-url")


def get_main_character(message, character_name, unlimited):
    headers, body = cp.configure_request(message, request_mode)

    url = "{}/trophy/character/find-main?apitoken={}&nickname={}&unlimited={}"\
        .format(api.url, api.apiToken, character_name, unlimited)
    response = cp.request_url(url, body, headers)

    return configure_message(response)


def configure_message(response):
    if response['error']:
        response.update({"log": response['msg']})
        return response

    print(response)

    if response[cp.status] == 'fail' and not response['error']:
        msg = "캐릭터를 찾지 못했습니다." + cp.add_admin_info(response[cp.process_time])
        response.update({"msg": msg, "log": msg})
        return response

    character = response[character_list][0]

    embed = discord.Embed(title="대표 캐릭터 검색 결과", description="  ", color=0x00ff56)
    embed.add_field(name="닉네임", value=character[nickname], inline=True)
    embed.add_field(name="순위", value="{}위".format(format(int(character[rank]), ",")), inline=True)
    embed.add_field(name="트로피", value="{}개".format(format(int(character[trophy]), ",")), inline=False)
    embed.set_thumbnail(url="attachment://profileimage.png")

    log = "대표 캐릭터 검색 결과\n닉네임: {}\n순위: {}\n트로피: {}\n프로필URL: {}" \
        .format(character[nickname], character[rank], character[trophy], character[profile_url])

    msg = str()
    if response[cp.admin]:
        msg = cp.add_admin_info(response[cp.process_time])
        log += cp.add_admin_info(response[cp.process_time])

    response.update({'error': False, 'log': log, 'embed': embed, 'msg': msg if response[cp.admin] else None})

    return response


async def send_message(result, channel):
    if result['error']:
        await channel.send(result['msg'], delete_after=30.0)
        return None

    if result[cp.status] == "fail":
        await channel.send(result['msg'], delete_after=30.0)
        return None

    if result[cp.ban]:
        return None

    character = result[character_list][0]
    urllib.request.urlretrieve(character[profile_url], character[nickname] + ".png")
    file = discord.File(character[nickname] + ".png", filename="profileimage.png")

    if result[cp.admin]:
        await channel.send(result['msg'], embed=result['embed'], file=file)
    else:
        await channel.send(embed=result['embed'], file=file, delete_after=60.0)

    log.update_log(result[cp.log_num], result['log'])
    return None
