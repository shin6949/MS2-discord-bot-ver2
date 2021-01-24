import datetime
import time
import discord
from discord import Colour
from discord.ext import tasks

# 별도 파일들
import ox
import log
import api_server_info
import minigame
import main_character_find as main_character

client = discord.Client()


# Bot initialize
@client.event
# on_ready는 봇을 다시 구성할 때도 호출 됨 (한번만 호출되는 것이 아님.)
async def on_ready():
    game = discord.Game("!설명서, !ox로 검색")
    await client.change_presence(status=discord.Status.online, activity=game)
    print("READY")


# message respond
@client.event
async def on_message(message):
    channel = message.channel

    # sender가 bot일 경우 ignore
    if message.author.bot:
        return None

    # 아무 검색 키워드를 입력하지 않은 경우
    if message.content == '!ox' or message.content == '!OX':
        await channel.send("입력한 키워드가 없습니다!", delete_after=10.0)
        log.insert_log(message, "입력한 키워드가 없습니다!", "ox")
        return None

    if message.content.startswith('!ox ') or message.content.startswith('!OX '):
        result = ox.get_ox(message, message.content.partition(' ')[2].lstrip())

        await ox.common_ox_processing(result, channel)

    if message.content.startswith('!ㅋ '):
        result = ox.get_ox_short(message, message.content.partition(' ')[2].lstrip())

        await ox.common_ox_processing(result, channel)

    if message.content == "!미겜":
        result = minigame.get_now_minigame(message)

        await minigame.common_mini_processing(result, channel)
        return None

    if message.content == "!다음미겜":
        result = minigame.get_next_minigame(message)

        await minigame.common_mini_processing(result, channel)
        return None

    if message.content.startswith('!메인 '):
        if message.content == "!메인 ":
            return None

        message_partition = message.content.partition(' ')
        keyword = message_partition[2]
        try:
            unlimited = "True" if message_partition[4] == "무한" else "False"
        except IndexError as ie:
            unlimited = "False"

        result = main_character.get_main_character(message, keyword, unlimited)
        await main_character.send_message(result, channel)
        return None


client.run(api_server_info.botToken)

