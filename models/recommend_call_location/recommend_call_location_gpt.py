from langchain.chat_models import AzureChatOpenAI

from models.common.util import get_weather_db, get_current_weather_info
from models.recommend_call_location.recommend_call_location_template import get_template_prompt
from models.recommend_call_location.util import parsing_address, get_address_by_lat_lng, get_call_demand


class RecommendCallLocationGpt:
    def __init__(self, azure_deployment="gpt-4", db_path="./data/weather_rapid.csv", call_demand_candidate_num=5):
        self.call_demand_candidate_num = call_demand_candidate_num
        self.chat = AzureChatOpenAI(azure_deployment=azure_deployment)
        self.weather_db = get_weather_db(db_path)

    def predict(self, driver_lat, driver_lng, current_time=None):
        driver_address = parsing_address(get_address_by_lat_lng([driver_lat, driver_lng])[0])
        current_recommend_call, call_after_30m_recommend_call = get_call_demand(driver_lat, driver_lng,
                                                                                max_num=self.call_demand_candidate_num)
        current_address = get_address_by_lat_lng(current_recommend_call)
        call_after_30m_address = get_address_by_lat_lng(call_after_30m_recommend_call)

        current_address_str_list = list(map(parsing_address, current_address))
        call_after_30m_address_str_list = list(map(parsing_address, call_after_30m_address))

        areaname_wide, areaname_city = driver_address.split(" ")[:2]

        weather_data = get_current_weather_info(weather_db=self.weather_db, areaname_wide=areaname_wide,
                                                areaname_city=areaname_city, current_time=current_time)

        prompt = get_template_prompt(
            driver_address=driver_address,
            current_address_str_list=current_address_str_list,
            call_after_30m_address_str_list=call_after_30m_address_str_list,
            weather_data=weather_data)

        chain = prompt | self.chat

        return chain.invoke({}).content


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()

    recommend_location_gpt = RecommendCallLocationGpt(
        azure_deployment="gpt-4",
        db_path="../../data/weather_rapid.csv"
    )

    resp = recommend_location_gpt.predict(
        driver_lat=37.508811,
        driver_lng=127.040978,
        current_time="2023-11-21T18:00"
    )

    print(resp)
