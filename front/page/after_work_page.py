import streamlit as st

from front import js_map
from front.model_controller import get_recommend_call_location


def after_work_page(picker_coord, default_current_time):
    st.header("기사님 수요밀집 지역 추천")
    st.image('resources/after_work_flow.png')
    img_col1, img_col2 = st.columns([3, 5])
    with img_col1:
        st.image('resources/situation2.png')
    with img_col2:
        col1, col2 = st.columns([5, 5])
        with col1:
            picker_lat = st.text_input("픽커 lat", picker_coord[0])
            current_time = st.text_input("시간 설정", default_current_time)
        with col2:
            picker_lon = st.text_input("픽커 lat", picker_coord[1])
        # 버튼 클릭 여부 확인
        if st.button("모델 예측", key="coord"):
            with st.spinner("Loading..."):
                recommend_result = get_recommend_call_location(lat=picker_lat, lon=picker_lon,
                                                               current_time=current_time)
                st.write(recommend_result)
                js_map.getMapWithPicker((picker_lat, picker_lon))
