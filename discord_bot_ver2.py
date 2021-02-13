import discord
from discord.ext import commands

# 별도 파일들
import api_server_info as api
import ox
import log
import minigame
import main_character_find as main_character
import special_function
import guild_information as guild
import character_information as character
import custom_message as custom
import boss
import legion_war as legion

prefix = "!"
bot = commands.Bot(command_prefix=prefix)
first_message = "데이터를 조회 중입니다."


@bot.event
async def on_ready():
    """
    로딩되거나 리로드 될 때 호출되는 함수

    :return: None
    """
    game = discord.Game("!설명서, !ox로 검색")
    await bot.change_presence(status=discord.Status.online, activity=game)
    print("READY")


@bot.command(name="ox", aliases=["OX"])
async def get_ox(ctx):
    """
    일반 OX 퀴즈 검색 결과를 반환하는 함수.

    :param ctx: 전체 메시지 객체
    :return: None
    """
    if ctx.message.content == prefix + "ox":
        msg = "입력한 키워드가 없습니다!"
        await ctx.send(msg, delete_after=10.0)
        log.insert_log(ctx.message, msg, "ox")
        return None

    chat = await ctx.channel.send(first_message)
    keyword = ctx.message.content.partition(' ')[2].lstrip()
    result = ox.get_ox(ctx, keyword)
    await ox.common_ox_processing(chat, result)
    return None


@bot.command(name="ㅋ")
async def get_ox_short(ctx):
    """
    짧은 명령어를 통한 OX 퀴즈 검색.
    짧은 명령어 허용이 되어 있는지 확인 필요.

    :param ctx: 전체 메시지 객체
    :return: None
    """
    sf = special_function.get_special_function_information(ctx)

    if special_function.judge_short_command(sf):
        if ctx.message.content == prefix + "ㅋ":
            msg = "입력한 키워드가 없습니다!"
            await ctx.channel.send(content=msg, delete_after=10.0)
            log.insert_log(ctx.message, msg, "ox")
            return None

        chat = await ctx.channel.send(first_message)
        keyword = ctx.message.content.partition(' ')[2].lstrip()
        result = ox.get_ox_short(ctx, keyword)
        await ox.common_ox_processing(chat, result)
    return None


@bot.command(name="미겜")
async def get_minigame(ctx):
    chat = await ctx.channel.send(first_message)
    result = minigame.get_now_minigame(ctx)
    await minigame.common_mini_processing(result, chat)
    return None


@bot.command(name="다음미겜")
async def get_next_minigame(ctx):
    chat = await ctx.channel.send(first_message)
    result = minigame.get_next_minigame(ctx)

    await minigame.common_mini_processing(result, chat)
    return None


@bot.command(name="메인")
async def get_main_character(ctx, *args):
    sf = special_function.get_special_function_information(ctx)

    if special_function.judge_trophy(sf):
        chat = await ctx.channel.send(first_message)

        keyword = args[0]
        if len(args) > 1:
            unlimited = "True" if args[1] == "무한" else "False"
        else:
            unlimited = "False"

        result = main_character.get_main_character(ctx, keyword, unlimited)
        await chat.delete()
        await main_character.send_message(result, ctx.channel)
    return None


@bot.command(name="필보")
async def get_bosses_soon_and_search(ctx):
    chat = await ctx.channel.send(first_message)
    keyword = ctx.message.content.partition(' ')[2].lstrip()

    if len(keyword) == 0:
        result = boss.get_bosses_soon(ctx)
        await boss.send_message(result, chat)
        return None
    else:
        try:
            result = boss.get_bosses_by_time(ctx, keyword)
            await boss.send_message(result, chat)
        except ValueError as ve:
            result = boss.get_bosses_by_name(ctx, keyword)
            await boss.send_message(result, chat)

    return None


@bot.command(name="다음필보")
async def get_bosses_next(ctx):
    chat = await ctx.channel.send(first_message)
    result = boss.get_bosses_next(ctx)
    await boss.send_message(result, chat)


@bot.command(name="군단")
async def get_legion_war_soon(ctx):
    chat = await ctx.channel.send(first_message)
    result = legion.get_legion_war_soon(ctx)
    await legion.send_message(result, chat)


@bot.command(name="다음군단")
async def get_legion_war_soon(ctx):
    chat = await ctx.channel.send(first_message)
    result = legion.get_legion_war_next(ctx)
    await legion.send_message(result, chat)


@bot.command(name="길트")
async def get_guild(ctx, *args):
    sf = special_function.get_special_function_information(ctx)

    if special_function.judge_trophy(sf):
        chat = await ctx.channel.send(first_message)

        if len(args) == 0:
            result = guild.get_guild(ctx, None)
            await guild.send_message_first_page(result, chat)
            return None
        else:
            result = guild.get_guild(ctx, args[0])
            await chat.delete()
            await guild.send_message_one(result, ctx.channel)
            return None


@bot.command(name="개트")
async def get_guild(ctx, *args):
    sf = special_function.get_special_function_information(ctx)

    if special_function.judge_trophy(sf):
        chat = await ctx.channel.send(first_message)

        if len(args) == 0:
            result = character.get_character(ctx, None)
            await character.send_message_first_page(result, chat)
            return None
        else:
            result = character.get_character(ctx, args[0])
            await chat.delete()
            await character.send_message_one(result, ctx.channel)
            return None


@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.content.startswith(prefix):
        result = custom.get_custom_message(message)
        await custom.send_msg(message.channel, result)
        return None

bot.run(api.botToken)

