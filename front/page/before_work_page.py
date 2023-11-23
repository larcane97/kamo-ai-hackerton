import streamlit as st

from front.model_controller import get_event_push


def before_work_page(default_current_time):
    st.header("출근 전 푸시 메세지")
    st.image('resources/before_work_flow.png')

    current_time = st.text_input("시간 설정", default_current_time)

    # 버튼 클릭 여부 확인
    if st.button("모델 예측", key="before_work_page"):
        with st.spinner("Loading..."):
            recommend_result = get_event_push(event_type="출근 전 알람", current_time=current_time)
            st.write(recommend_result)
