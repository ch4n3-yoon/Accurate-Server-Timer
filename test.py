import json
import time
import pytz
import pprint
import requests
import logging

from datetime import datetime, timezone, timedelta
from http.cookiejar import http2time


def get_server_time(session: requests.Session):
    local_timezone = pytz.timezone('Asia/Seoul')

    url = 'http://sugang.khu.ac.kr/blank.html?fake=1'
    resp = session.get(url, timeout=10)

    # Fri, 22 Jan 2021 04:00:01 GMT
    raw_server_time = resp.headers['Date']
    server_time = datetime.utcfromtimestamp(http2time(raw_server_time))\
        .replace(tzinfo=timezone.utc)\
        .astimezone(tz=local_timezone)

    return server_time


def get_accurate_server_time(session: requests.Session):
    """
    서버시간과의 오차 0.01초로 줄이는 함수
    """
    previous_time = get_server_time(session)
    while True:
        time.sleep(0.001)
        current_time = get_server_time(session)

        if previous_time != current_time:
            return current_time
        else:
            previous_time = current_time


def main():
    delta = 0.1
    re_calculate = False
    session = requests.Session()
    logging.basicConfig(level=logging.INFO)

    while True:
        server_time = get_accurate_server_time(session)
    
        execute_seconds = 0
        while True:
            guessed_server_time = server_time + timedelta(seconds=execute_seconds)
            logging.info(f'guessed server time : {guessed_server_time}')
            time.sleep(delta)
            execute_seconds += delta

            if execute_seconds % 30 == 0:
                break


if __name__ == '__main__':
    main()
