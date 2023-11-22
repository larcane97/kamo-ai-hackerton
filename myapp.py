import streamlit as st

import js_map
from model_controller import get_recommend_rest_location
picker_coord = [37.4798219868059,126.980942740446]

st.title('Picker Mate')
st.header('헤 더')
def makePage(situation):
    if situation=="출근 전":
        st.write("hello")
    elif situation=="출근 후":
        st.write("hi")
    elif situation=="운행 중":
        st.write("bye")
    elif situation=="수행 완료 & 오후 시간":
        col1, col2 = st.columns([5,5])
        with col1:
            picker_lat = st.text_input("픽커 lat", picker_coord[0])
        with col2:
            picker_lon = st.text_input("픽커 lat",  picker_coord[1])
        # 버튼 클릭 여부 확인
        if st.button("데이터 불러오기", key="coord"):
            with st.spinner("Loading..."):
                recommend_result = get_recommend_rest_location(lat=picker_lat, lon=picker_lon)
                st.write(recommend_result)
                js_map.getMapWithMarker(picker_coord, "helloo")


    elif situation=="수행 완료 & 연속 3시간 이상 근무 시":
        st.write("ye")

with st.sidebar:
    selected_option = st.sidebar.selectbox("상황 선택", ["출근 전", "출근 후", "운행 중", "수행 완료 & 오후 시간", "수행 완료 & 연속 3시간 이상 근무 시"])

makePage(selected_option)