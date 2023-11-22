from langchain.chat_models import AzureChatOpenAI

from models.recommend_location.prompt import get_template_prompt
from models.recommend_location.util import parsing_address, get_address_by_lat_lng, get_call_demand


class RecommendLocationGpt:
    def __init__(self, azure_deployment="gpt-4"):
        self.chat = AzureChatOpenAI(azure_deployment=azure_deployment)

    def predict(self, driver_lat, driver_lng):
        driver_address = parsing_address(get_address_by_lat_lng([driver_lat, driver_lng])[0])
        current_recommend_call, call_after_30m_recommend_call = get_call_demand(driver_lat, driver_lng)
        current_address = get_address_by_lat_lng(current_recommend_call)
        call_after_30m_address = get_address_by_lat_lng(call_after_30m_recommend_call)

        current_address_str_list = list(map(parsing_address, current_address))
        call_after_30m_address_str_list = list(map(parsing_address, call_after_30m_address))

        prompt = get_template_prompt(
            driver_address=driver_address,
            current_address_str_list=current_address_str_list,
            call_after_30m_address_str_list=call_after_30m_address_str_list)

        chain = prompt | self.chat

        return chain.invoke({})
