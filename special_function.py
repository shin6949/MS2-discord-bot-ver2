import common_process as cp
import api_server_info as api
import response_parameter as rp

request_mode = ""
service_name = 'special-function'
information_key = rp.get_param(service_name, "information")
short_command_key = rp.get_param(service_name, "short-command")
trophy_key = rp.get_param(service_name, 'trophy')


def get_special_function_information(message):
    headers, body = cp.configure_request(message, request_mode)
    url = "{}/special/get?apitoken={}".format(api.url, api.apiToken)

    response = cp.request_url(url, body, headers)

    return response


def judge_short_command(response):
    return True if response[information_key][short_command_key] else False


def judge_trophy(response):
    return True if response[information_key][trophy_key] else False

