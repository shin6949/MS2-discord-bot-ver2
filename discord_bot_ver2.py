import datetime
import time
import discord
from discord import Colour
from discord.ext import tasks

# 별도 파일들
import ox
import log
import api_server_info

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

    if message.content == '!ox ' or message.content == '!OX ':
        await channel.send("입력한 키워드가 없습니다!", delete_after=10.0)
        return None

    if message.content.startswith('!ox ') or message.content.startswith('!OX '):
        result = ox.get_ox(message, message.content.partition(' ')[2].lstrip())

        if result['ban']:
            return None

        if result['admin']:
            await channel.send(result['msg'])
        else:
            await channel.send(result['msg'], delete_after=60.0)

        log.update_log(result['query-num'], None if result['ban'] else result['msg'])
        return None


client.run(api_server_info.botToken)

