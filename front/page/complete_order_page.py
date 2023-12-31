import streamlit as st

from front import js_map
from front.model_controller import get_recommend_rest_location
import re

def complete_order_page(picker_coord, default_current_time):
    st.header("오더 수행 완료 후 메세지")
    st.image('resources/situation3-1.png')
    img_col1, img_col2 = st.columns([3, 5])
    with img_col1:
        st.image('resources/situation3.png')
    with img_col2:
        col1, col2 = st.columns([5, 5])
        with col1:
            picker_lat = st.text_input("픽커 lat", picker_coord[0])
            picker_lon = st.text_input("픽커 lon", picker_coord[1])
        with col2:
            driver_type = st.selectbox("기사 타입", ["quick", "wheel", "taxi"])

            current_time = st.text_input("시간 설정", default_current_time)
            st.text("점심시간 : 12~14시")
            st.text("저녁시간 : 18~20시")

        # 버튼 클릭 여부 확인
        if st.button("모델 예측", key="coord"):
            with st.spinner("Loading..."):
                recommend_result = get_recommend_rest_location(
                    lat=float(picker_lat), lon=float(picker_lon), driver_type=driver_type, current_time=current_time)

                pattern = r'<(.*?)>'
                candidate_list = re.findall(pattern, recommend_result[0])
                # print(candidate_list)
                # print(recommend_result[1])
                poi_dict = dict()
                for name in candidate_list:
                    poi_dict[name] = "37,127"

                for e in recommend_result[1]:
                    poi_name = e['poi_name']
                    if poi_name in poi_dict:
                        poi_dict[poi_name] = e['address'].rstrip(")").split("(")[1]

                st.write(recommend_result[0])
                # js_map.getMapWithPicker((picker_lat, picker_lon))
                js_map.getMapWithMarkerList((picker_lat, picker_lon), poi_dict)
