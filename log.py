import requests
import json
import api_server_info as api


def configure_headers():
    return {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json'
    }


def update_log(query_num, msg):
    body = {
        "logId": query_num,
        "response": msg
    }

    url = "{}/log/update-response?apitoken={}".format(api.url, api.apiToken)
    requests.post(url, data=json.dumps(body), headers=configure_headers())


def insert_log(message, response, call_value):
    body = {
        "query": message.content,
        "response": response,
        "callValue": call_value,
        "isDm": True if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>" else False,
        "userId": message.author.id,
        "serverId": None if str(type(message.channel)) == "<class 'discord.channel.DMChannel'>" else message.guild.id
    }

    url = "{}/log/insert?apitoken={}".format(api.url, api.apiToken)
    requests.post(url, data=json.dumps(body), headers=configure_headers())

