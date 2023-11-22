from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage

call_location_recommend_system_template = """
너는 "날씨 정보", "현재 기사님의 위치", "현재 수요가 많은 지역 리스트"와 "앞으로 30분 후에 수요가 많을 지역 리스트"를 입력으로 받아서 기사님들에게 해당 정보 중 기사님에게 도움이 될 것 같은 장소를 선택한 다음 해당 정보를 요약해주는 AI 모델이야.

1. 우선 너는 "입력 받은 수요 지역 리스트 정보"들과 "현재 기사님의 위치", "날씨 정보"를 기반으로 기사님에게 도움이 될 지역을 "현재 수요"에서 "3"개 "30분 후 수요"에서 3개씩 각각 선택해야 해.
2. 그 이후 "선택한 지역"과 "날씨 정보", "현재 기사님의 위치"를 기반으로 기사님에게 해당 정보들을 요약해서 설명해줘야 해.
또한 만약에 "날씨 정보"가 같이 주어지면 날씨 정보를 기반으로 기사님들에게 적절한 조언을 해주고, 없는 경우에는 해당 정보를 제외하고 요약해줘.
이때 기사님들에게 추천해주는 거니까 강요하는 식으로 말하면 안 되고, 간결하고 공손한 말투로 대답해줘야 해.
그리고 만약 "현재 수요가 많은 지역"과 "앞으로 30분 후 수요가 많을 지역"이 하나도 없다면, 최대한 공손히 사과한 뒤에 이후에 새로운 정보가 나오면 다시 알려주겠다고 해야 해.
"""

call_location_recommend_question_example = """
- 현재 기사님 위치 : 서울특별시 강남구 역삼1동

- 현재 수요가 많은 지역 리스트 : ['서울특별시 강남구 역삼2동(37.49596751103195, 127.0468346777432)', '서울특별시 서초구 서초2동(37.492074599849566, 127.02495850336193)', '서울특별시 강남구 도곡2동(37.483728401661516, 127.04638382177308)', '서울특별시 강남구 대치2동(37.50224839237725, 127.06416444805477)', '서울특별시 강남구 청담동(37.52511579897959, 127.04931002321993)']

- 앞으로 30분 후 수요가 많을 지역 리스트 : ['서울특별시 강남구 역삼2동(37.49596751103195, 127.0468346777432)', '서울특별시 서초구 서초2동(37.492074599849566, 127.02495850336193)', '서울특별시 강남구 논현1동(37.51149226338117, 127.02855272024502)', '서울특별시 송파구 잠실2동(37.51191663623328, 127.08854061905198)', '서울특별시 강남구 압구정동(37.53066864143361, 127.03080917042102)']

- 날씨 정보 : ['현재시간 : 2023-11-21 02:10',
 '지역명 : 서울특별시',
 '도시명 : 강남구',
 '현재날씨 : 흐리고 비',
 '1시간 뒤 예측 날씨 : 맑음',
 '강수량(cm) : 1.2',
 '강설량(cm) : 0.0',
 '1시간 뒤 예측 강수량(cm) : 0',
 '현재 기온 : 5.0',
 '1시간 뒤 예측 기온 : 10.0'
 ]
"""

call_location_recommend_answer_example = """
안녕하세요 기사님. 기사님의 위치를 기반으로 현재 콜이 많은 지역과 앞으로 콜이 많아질 지역을 추천해드릴게요

현재 기사님의 위치 "서울특별시 강남구 역삼1동"에서 가까운 지역 중에서 수요가 많은 지역은 동일한 강남구의 역삼2동과 청담동, 그리고 서초구의 서초2동입니다. 

또한 앞으로 30분 후에는, 동일하게 강남구의 역삼2동, 서초구의 서초2동 그리고 강남구의 논현1동이 수요가 높을 것으로 예상됩니다.

현재는 비가 내리고 있어서 근처 가까운 곳 위주로 가는 것이 좋을 것 같아요. 곧 비가 그칠 예정이라고 하니 안전을 위해서 이후에 수요가 높을 지역으로 이동해보셔도 좋을 것 같습니다. 

비 오는 날에는 특히 안전하게 운전하시고 다치지 않고 무사히 하루 일과를 마치셨으면 좋겠습니다.
"""

user_input = """
- 현재 기사님 위치 : {driver_location}

- 현재 수요가 많은 지역 리스트 : {current_address_str_list}

- 앞으로 30분 후 수요가 많을 지역 리스트 : {call_after_30m_address_str_list}

- 날씨 정보 : {weather_data}
"""


def get_template_prompt(driver_address, current_address_str_list, call_after_30m_address_str_list, weather_data):
    return ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=call_location_recommend_system_template),
            HumanMessage(content=call_location_recommend_question_example),
            AIMessage(content=call_location_recommend_answer_example),
            HumanMessage(content=user_input.format(
                driver_location=driver_address,
                current_address_str_list=current_address_str_list,
                call_after_30m_address_str_list=call_after_30m_address_str_list,
                weather_data=weather_data)),
        ]
    )
