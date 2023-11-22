import pandas as pd
from langchain.chat_models import AzureChatOpenAI

from models.common.util import get_weather_db, get_current_weather_info
from models.event_push.event_push_template import get_template_prompt
from models.recommend_call_location.util import parsing_address, get_address_by_lat_lng


class EventPushGpt:
    def __init__(self, azure_deployment="gpt-4"):
        self.chat = AzureChatOpenAI(azure_deployment=azure_deployment)
        self.weather_db = get_weather_db()

        # dummy db
        self.driver_db = {1:
                              {"driver_lat": 37.508811,
                               "driver_lng": 127.040978}
                          }

    ## event_type : ["우천 알람", "출근 전 알람", "장시간 근무 알람"]
    def predict(self, event_type, driver_id, current_time):
        driver_data = self.driver_db[driver_id]
        driver_lat, driver_lng = driver_data["driver_lat"], driver_data["driver_lng"]

        driver_address = parsing_address(get_address_by_lat_lng([driver_lat, driver_lng])[0])
        areaname_wide, areaname_city = driver_address.split(" ")[:2]

        weather_data = get_current_weather_info(weather_db=self.weather_db, areaname_wide=areaname_wide,
                                                current_time=current_time)

        prompt = get_template_prompt(event_type=event_type, driver_location=driver_address, weather_data=weather_data)
        chain = prompt | self.chat

        return chain.invoke({}).content
