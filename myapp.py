# import streamlit as st
#
# import js_map
# from model_controller import get_recommend_rest_location, get_recommend_call_location, get_recommend_cafe_loaction
# picker_coord = [37.4798219868059,126.980942740446]
# st.title('Picker Mate')
# # st.header('헤 더')
# def makePage(situation):
#     if situation=="출근 전":
#         st.write("hello")
#     elif situation=="출근 후":
#         st.image('resources/situation3-1.png')
#         img_col1, img_col2 = st.columns([3, 5])
#         with img_col1:
#             st.image('resources/situation2.png')
#         with img_col2:
#             col1, col2 = st.columns([5,5])
#             with col1:
#                 picker_lat = st.text_input("픽커 lat", picker_coord[0])
#             with col2:
#                 picker_lon = st.text_input("픽커 lat",  picker_coord[1])
#             # 버튼 클릭 여부 확인
#             if st.button("데이터 불러오기", key="coord"):
#                 with st.spinner("Loading..."):
#                     recommend_result = get_recommend_call_location(lat=picker_lat, lon=picker_lon)
#                     st.write(recommend_result)
#                     js_map.getMapWithPicker(picker_coord)
#
#     elif situation=="운행 중":
#         st.write("bye")
#
#     elif situation=="수행 완료 & 오후 시간":
#         st.image('resources/situation3-1.png')
#         img_col1,img_col2 = st.columns([3,5])
#         with img_col1:
#             st.image('resources/situation3.png')
#         with img_col2:
#             col1, col2 = st.columns([5,5])
#             with col1:
#                 picker_lat = st.text_input("픽커 lat", picker_coord[0])
#             with col2:
#                 picker_lon = st.text_input("픽커 lat",  picker_coord[1])
#             # 버튼 클릭 여부 확인
#             if st.button("데이터 불러오기", key="coord"):
#                 with st.spinner("Loading..."):
#                     recommend_result = get_recommend_rest_location(lat=picker_lat, lon=picker_lon)
#
#                     print_list =[]
#                     coord_list = []
#                     for list in recommend_result:
#                         print_list.append([list[0], list[1]])
#                         coord_list.append([list[0], list[2]])
#                     st.write(print_list)
#                     js_map.getMapWithMarkerList(picker_coord, coord_list)
#
#     elif situation=="수행 완료 & 연속 3시간 이상 근무 시":
#         st.image('resources/situation3-1.png')
#         img_col1, img_col2 = st.columns([3, 5])
#         with img_col1:
#             st.image('resources/situation3.png')
#         with img_col2:
#             col1, col2 = st.columns([5, 5])
#             with col1:
#                 picker_lat = st.text_input("픽커 lat", picker_coord[0])
#             with col2:
#                 picker_lon = st.text_input("픽커 lat", picker_coord[1])
#             # 버튼 클릭 여부 확인
#             if st.button("데이터 불러오기", key="coord"):
#                 with st.spinner("Loading..."):
#                     recommend_result = get_recommend_cafe_loaction(lat=picker_lat, lon=picker_lon)
#                     print_list = []
#                     coord_list = []
#                     for list in recommend_result:
#                         print_list.append([list[0], list[1]])
#                         coord_list.append([list[0], list[2]])
#                     st.write(print_list)
#                     js_map.getMapWithMarkerList(picker_coord, coord_list)
#
# with st.sidebar:
#     selected_option = st.sidebar.selectbox("상황 선택", ["출근 전", "출근 후", "운행 중", "수행 완료 & 오후 시간", "수행 완료 & 연속 3시간 이상 근무 시"])
#
# makePage(selected_option)