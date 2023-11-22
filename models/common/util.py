from datetime import datetime

import pandas as pd
import pytz


def get_current_kst_time():
    # 현재 시간을 UTC로 얻기
    current_time_utc = datetime.utcnow()

    # UTC+9 타임존으로 변환
    utcplus9_timezone = pytz.timezone('Asia/Seoul')
    current_time_utcplus9 = current_time_utc.replace(tzinfo=pytz.utc).astimezone(utcplus9_timezone)

    # 문자열로 포맷팅
    result_string = current_time_utcplus9.strftime('%Y-%m-%dT%H:00')

    return result_string


def convert_utc_to_kst(utc_string):
    # UTC로 파싱
    utc_time = datetime.strptime(utc_string, '%Y-%m-%d %H:%M:%S %Z')
    utc_time = pytz.utc.localize(utc_time)

    # UTC+9 타임존으로 변환
    utcplus9_timezone = pytz.timezone('Asia/Seoul')
    utcplus9_time = utc_time.astimezone(utcplus9_timezone)

    # 변환된 시간을 문자열로 포맷팅
    result_string = utcplus9_time.strftime('%Y-%m-%dT%H:00')

    return result_string


def set_weather_key(select_timestamp, wide, city):
    key_list = [select_timestamp]

    if wide is not None and not wide == "-":
        key_list.append(wide)

    if city is not None and not city == "-":
        key_list.append(city)

    return "__".join(key_list)


def get_weather_db(path="./data/weather_rapid.csv") -> dict:
    weather = pd.read_csv(path)

    weather = weather[
        ["select_timestamp", "areaname_wide", "areaname_city", "wtext", "wtext_1hr", "rain", "snow", "wtext_1hr",
         "rain_1hr", "temp", "temp_1hr"]]

    weather["snow"] = weather["snow"].fillna(0)
    weather["rain"] = weather["rain"].fillna(0)
    weather["select_timestamp"] = weather["select_timestamp"].apply(convert_utc_to_kst)

    weather["key"] = weather[["select_timestamp", "areaname_wide", "areaname_city"]].apply(
        lambda x: set_weather_key(
            select_timestamp=x.get("select_timestamp"),
            wide=x.get("areaname_wide"),
            city=x.get("areaname_city")
        ), axis=1
    )

    weather = weather.rename(
        columns={
            "select_timestamp": "현재시간",
            "areaname_wide": "지역명",
            "areaname_city": "도시명",
            "wtext": "현재날씨",
            "wtext_1hr": "1시간 뒤 예측 날씨",
            "rain": "강수량(cm)",
            "snow": "강설량(cm)",
            "rain_1hr": "1시간 뒤 예측 강수량(cm)",
            "temp" : "현재 기온",
            "temp_1hr" : "1시간 뒤 예측 기온"
        }
    )

    weather = weather.drop_duplicates(subset='key', keep='first')
    return weather.set_index("key").to_dict(orient="index")


def get_current_weather_info(weather_db: pd.DataFrame, current_time=None, areaname_wide="서울특별시", areaname_city=None):
    if current_time is None:
        current_time = get_current_kst_time()

    key = set_weather_key(current_time, areaname_wide, areaname_city)

    data = weather_db.get(key)

    if data is None:
        return []

    result = []
    for key, value in data.items():
        result.append(f"{key} : {value}")

    return result
