from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage

call_location_recommend_system_template = """
너는 "현재 기사님의 위치", "현재 수요가 많은 지역 리스트"와 "앞으로 30분 후에 수요가 많을 지역 리스트"를 입력으로 받아서 기사님들에게 해당 정보를 요약해주는 AI 모델이야.
너는 입력 받은 수요 지역 리스트 정보를 기반으로 현재 수요가 많은 지역, 앞으로 수요가 많을 지역들에 대해 설명해주어야 해.
이때 기사님들에게 추천해주는 거니까 강요하는 식으로 말하면 안 되고, 간격하고 공손한 말투로 대답해줘야 해
"""

call_location_recommend_question_example = """
- 현재 기사님 위치 : 서울특별시 강남구 역삼1동

- 현재 수요가 많은 지역 리스트 : ['서울특별시 강남구 논현1동', '서울특별시 종로구 종로1.2.3.4가동', '경기도 성남시 분당구 판교동']

- 앞으로 30분 후 수요가 많을 지역 리스트 : ['서울특별시 강남구 청담동', '서울특별시 송파구 가락본동', '서울특별시 광진구 광장동']
"""

call_location_recommend_answer_example = """
안녕하세요 기사님. 기사님의 위치를 기반으로 현재 콜이 많은 지역과 앞으로 콜이 많아질 지역을 추천해드릴게요

현재 기사님의 위치 "서울특별시 강남구 역삼1동"에서 가까운 지역 중에서 수요가 많은 지역은 동일한 강남구의 논현1동과 종로구의 종로, 경기도의 성남시 분당구입니다.

또한 앞으로 30분 후에 콜 예측을 수행했을 때에는, 강남구의 청담동, 송파구의 가락본동, 광진구의 광장동이 수요가 높을 것으로 예상됩니다.

논현1동은 현재 지역과 거리가 그리 멀지 않으니 해당 지역에 가서 대기해보셔도 좋을 것 같습니다.
또한 잠깐 다른 업무를 보셔야 한다면 업무를 보신 다음에 강남구의 청담동에 가보셔도 좋을 것 같습니다.
"""

user_input = """
- 현재 기사님 위치 : {driver_location}

- 현재 수요가 많은 지역 리스트 : {current_address_str_list}

- 앞으로 30분 후 수요가 많을 지역 리스트 : {call_after_30m_address_str_list}
"""


def get_template_prompt(driver_address, current_address_str_list, call_after_30m_address_str_list):
    ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=call_location_recommend_system_template),
            HumanMessage(content=call_location_recommend_question_example),
            AIMessage(content=call_location_recommend_answer_example),
            HumanMessage(content=user_input.format(
                driver_location=driver_address,
                current_address_str_list=current_address_str_list,
                call_after_30m_address_str_list=call_after_30m_address_str_list)),
        ]
    )
