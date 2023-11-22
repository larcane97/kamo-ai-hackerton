import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import AzureChatOpenAI
import models.recommend_rest_loaction.util as util
from models.recommend_rest_loaction.recommend_rest_template import get_template_prompt
from collections import defaultdict
import csv



class RecommendCafeGpt:
    def __init__(self, azure_deployment="gpt-4", csv_path = "./data/poi_coord.csv"):
        self.chat = AzureChatOpenAI(azure_deployment=azure_deployment)
        self.db = pd.read_csv(csv_path)

    # lat = 37
    def predict(self, driver_lat, driver_lon):

        store_map = defaultdict()
        store_list = ''
        for _, row in self.db.iterrows():
            rest_lat, rest_lon = eval(row['coord'])
            distance = util.get_distance((driver_lat, driver_lon), (float(rest_lat), float(rest_lon)))
            scores = eval(row['scores'])
            sum_of_values = sum(float(value) for value in scores)
            average = sum_of_values / len(scores)

            if (distance<500):
                store_list+= f"{row['poi_name']} | {row['name2']} | {average}| {row['reviews']} || "
                store_map[row['poi_name']] = eval(row['coord'])


        prompt = get_template_prompt(store_list)
        chain = prompt | self.chat
        result = chain.invoke({}).to_json()['kwargs']['content']
        resultList = []
        split = result.split("|")
        for rest in split:
            result_poi_name, result_recommend = rest.split("-")
            resultList.append([result_poi_name, result_recommend, store_map[result_poi_name]])
        return resultList


