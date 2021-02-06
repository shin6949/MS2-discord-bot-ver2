import pymysql
import ox
import response_parameter
import requests
import json
import api_server_info as api
import pandas as pd

# 공통 상수들
query = response_parameter.get_param('request', 'query')
call_value = response_parameter.get_param('request', 'call-value')
is_dm = response_parameter.get_param('request', 'is-dm')
user_id = response_parameter.get_param('request', 'user-id')
server_id = response_parameter.get_param('request', 'server-id')

ban = response_parameter.get_param('common', 'ban')
count = response_parameter.get_param('common', 'count')
admin = response_parameter.get_param('common', 'admin')
process_time = response_parameter.get_param('common', 'process-time')
log_num = response_parameter.get_param('common', 'log-num')
status = response_parameter.get_param('common', 'status')


def configure_request(message):
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json'
    }

    body = {
        query: message,
        call_value: "ox",
        is_dm: True,
        user_id: 363949839471476736,
        server_id: None
    }

    return headers, body


def request_url(url, body, headers):
    r = requests.get(url, data=json.dumps(body), headers=headers)
    response = json.loads(r.text)

    return response


if __name__ == "__main__":
    conn = pymysql.connect(host="", port=3306, user="", password="", db="MS2OX")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT QueryTime, Query FROM log WHERE Query_type = 'ox'"
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()

    print(f"{len(result)}개의 쿼리 시작")
    each_keyword = list()
    each_process_time = list()

    for i in result:
        keyword = i['Query'].partition(' ')[2].lstrip()
        headers, body = configure_request(i['Query'])

        url = "{}/ox/search?apitoken={}&keyword={}".format(api.url, api.apiToken, keyword)
        response = request_url(url, body, headers)

        each_keyword.append(keyword)
        each_process_time.append(int(response['process-time']))

        if len(each_process_time) % 100 == 0:
            count = len(each_process_time)
            one_count_list = each_process_time[count-100:]
            average = sum(one_count_list) / 100

            print(f"{count}회 완료\n"
                  f"{count - 100}~{count}회 총 소요시간: {sum(one_count_list)}ms\n"
                  f"{count - 100}~{count}회 평균: {average}ms\n"
                  f"{count - 100}~{count}회 최대: {max(one_count_list)}ms\n"
                  f"{count - 100}~{count}회 최소: {min(one_count_list)}ms\n")

    data = {'Keyword': each_keyword, 'Process Time': each_process_time}
    df = pd.DataFrame(data)

    print(f"평균 처리 시간: {sum(each_process_time)/len(each_process_time)}\n"
          f"최대 값: {max(each_process_time)}\n"
          f"최소 값:{min(each_process_time)}\n")

    df.to_csv('./data.csv')
