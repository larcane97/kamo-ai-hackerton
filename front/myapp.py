import streamlit as st

from front.page.after_work_page import after_work_page
from front.page.before_work_page import before_work_page
from front.page.complete_order_page import complete_order_page
from front.page.rest_alert_page import rest_alert
from front.page.weather_alert import weather_alert

picker_coord = [37.4798219868059, 126.980942740446]
picker_coord_2 = [37.4994,  127.0269]
default_current_time = "2023-11-21T18:00"

st.title('Picker Mate')


def makePage(situation):
    if situation == "출근 전":
        before_work_page(default_current_time=default_current_time)
    elif situation == "출근 후 & 콜 대기 중":
        after_work_page(picker_coord=picker_coord, default_current_time=default_current_time)

    elif situation == "운행 중":
        weather_alert(default_current_time=default_current_time)

    elif situation == "운행 완료":
        complete_order_page(picker_coord=picker_coord, default_current_time=default_current_time)

    elif situation == "연속 3시간 이상 근무 시":
        rest_alert(default_current_time=default_current_time)


with st.sidebar:
    selected_option = st.sidebar.selectbox("상황 선택", ["출근 전", "출근 후 & 콜 대기 중", "운행 중", "운행 완료", "연속 3시간 이상 근무 시"])

makePage(selected_option)
