import pickle
from datetime import datetime

import numpy as np
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
import models.recommend_rest_loaction.util as util
from models.common.util import get_current_kst_time, find_top_k_similarities, get_weather_db, get_current_weather_info
from models.recommend_call_location.util import get_address_by_lat_lng, parsing_address
from models.recommend_rest_loaction.recommend_rest_template import get_template_prompt


class RecommendRestGpt:
    def __init__(self, azure_deployment="gpt-4",
                 poi_db_path="./data/poi_review_with_embedding.pkl",
                 weather_db_path="./data/weather_rapid.csv"):
        self.event_type = None
        self.chat = AzureChatOpenAI(azure_deployment=azure_deployment)
        self.embedding_model = AzureOpenAIEmbeddings(azure_deployment="text-embedding-ada-002", chunk_size=1000)

        self.weather_db = get_weather_db(weather_db_path)
        with open(poi_db_path, "rb") as f:
            self.poi_db = pickle.load(f)

        self.distance_threshold_meters_dict = {
            "quick": 3000,
            "taxi": 3000,
            "wheel": 1000
        }

        self.driver_rest_poi = {
            "식사": "가격이 싸고, 웨이팅이 없으며 음식 종류가 많고 {time}시간에 혼자 가기 좋은 식당을 추천해 줘.",
            "휴식": "사람이 많지 않고, 시끄럽지 않으면서 웨이팅이 없고 휴식하기에 좋은 장소를 추천해 줘."
        }

    def get_query_embedding(self, current_time):
        current_hour = datetime.strptime(current_time, "%Y-%m-%dT%H:00").hour
        if 12 <= current_hour <= 14:
            self.event_type = "식사"
            query = self.driver_rest_poi["식사"].format(time="점심")
        elif 18 <= current_hour <= 20:
            self.event_type = "식사"
            query = self.driver_rest_poi["식사"].format(time="저녁")
        else:
            self.event_type = "휴식"
            query = self.driver_rest_poi["휴식"]

        query_embedding = self.embedding_model.embed_query(query)

        return np.array(query_embedding)

    def get_document_embedding(self, poi_candidate):
        doc_embeddings = []
        for key, value in poi_candidate.items():
            doc_embedding = np.array(value["embedding"]).reshape(1, -1)
            doc_embeddings.append(doc_embedding)

        return np.vstack(doc_embeddings)

    def get_recommend_poi(self, top_k_indices, poi_candidate):
        def _parsing_address(poi_info: dict):
            addresses = [addr for addr in
                         [poi_info.get('hname1', ''), poi_info.get('hname2', ''), poi_info.get('hname3', '')] if
                         addr != '']
            lat_lng = f"({poi_info['coord'][0]}, {poi_info['coord'][1]})"

            return " ".join(addresses) + lat_lng

        poi_candidate_list = list(poi_candidate.items())
        recommend_poi = {}
        for index in top_k_indices:
            key, value = poi_candidate_list[index]
            new_value = {"address": _parsing_address(value)}
            for k in ["poi_name", "distance", "categories", "time_list", "reviews"]:
                new_value[k] = value[k]

            recommend_poi[key] = new_value

        return list(recommend_poi.values())

    def predict(self, driver_lat, driver_lon, driver_type="quick", current_time=None):
        if current_time is None:
            current_time = get_current_kst_time()

        # 01. api 및 db 조회로 기타 정보 획득
        raw_driver_location = get_address_by_lat_lng([driver_lat, driver_lon])[0]
        driver_location = parsing_address(raw_driver_location)
        weather_info = get_current_weather_info(self.weather_db, current_time=current_time,
                                                areaname_wide=raw_driver_location['name1'],
                                                areaname_city=raw_driver_location.get('name2'))

        # 02. 현재 기사 위치를 기반으로 근처 장소 검색
        poi_candidate = util.get_poi_by_distances(
            self.poi_db, driver_lat, driver_lon,
            distance_threshold_meters=self.distance_threshold_meters_dict[driver_type])

        # 03. 검색된 장소를 기반으로 vector search 진행
        query_embedding = self.get_query_embedding(current_time)
        doc_embeddings = self.get_document_embedding(poi_candidate)
        top_k_indices, _ = find_top_k_similarities(query_embedding, doc_embeddings, k=5)
        recommend_poi = self.get_recommend_poi(top_k_indices, poi_candidate)

        # 04. 프롬프트 생성
        prompt = get_template_prompt(
            event_type=self.event_type,
            driver_location=driver_location,
            weather_info=weather_info,
            location_info=recommend_poi
        )

        # 05. 예측 수행
        chain = prompt | self.chat
        result = chain.invoke({}).content
        return result
        # print(result)
        #
        # coordDict = dict()
        # # ++. 근처 장소 좌표 추출
        # for e in recommend_poi:
        #
        #     print(e.get('poi_name'), e.get('address').rstrip(')').split('(')[1])
        #     coordDict[e.get('poi_nane')] = e.get('address').rstrip(')').split('(')[1]
        #
        # resultList = []
        #
        # for e in result:
        #     print(e)

        # split = result.split("|")
        # for rest in split:
        #     result_poi_name, result_recommend = rest.split("-")
        #     resultList.append([result_poi_name, result_recommend, store_map[result_poi_name]])
        # return resultList


if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    recommend_rest_gpt = RecommendRestGpt(
        azure_deployment="gpt-4",
        poi_db_path="../../data/poi_review_with_embedding.pkl",
        weather_db_path="../../data/weather_rapid.csv"
    )

    resp = recommend_rest_gpt.predict(
        driver_lat=37.508811,
        driver_lon=127.040978,
        current_time="2023-11-21T18:00"
    )

    print(resp)
